"""Update Cam's position in build/data.json from his public Garmin inReach feed.
Run by .github/workflows/refresh.yml. Only touches the "today" fields; the rest of
data.json (route, plan, towns) comes from the hourly rebuild."""
import json, math, os, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'data.json')
FEED = 'https://share.garmin.com/Feed/Share/HJZZX'

def hav(a, b, c, d):
    r = math.radians
    x = math.sin(r(c - a) / 2) ** 2 + math.cos(r(a)) * math.cos(r(c)) * math.sin(r(d - b) / 2) ** 2
    return 7917.6 * math.asin(math.sqrt(x))

def pings(kml):
    out = []
    for pm in re.findall(r'<Placemark[^>]*>(.*?)</Placemark>', kml, re.S):
        w = re.search(r'<when>([^<]+)</when>', pm)
        c = re.search(r'<Point[^>]*>.*?<coordinates>\s*([-\d.]+),([-\d.]+)', pm, re.S)
        if w and c:
            t = datetime.fromisoformat(w.group(1).strip().replace('Z', '+00:00'))
            out.append((t, float(c.group(2)), float(c.group(1))))
    return sorted(out)

def project(route, lat, lon, lo, hi):
    best = None
    for i in range(len(route) - 1):
        m1, a1, o1 = route[i]; m2, a2, o2 = route[i + 1]
        if m2 < lo or m1 > hi: continue
        for k in range(5):
            f = k / 5; m = m1 + f * (m2 - m1)
            d = hav(lat, lon, a1 + f * (a2 - a1), o1 + f * (o2 - o1))
            if best is None or d < best[0]: best = (d, m)
    return best

def main(kml=None):
    D = json.load(open(P))
    if kml is None:
        since = (datetime.now(timezone.utc) - timedelta(hours=20)).strftime('%Y-%m-%dT%H:%MZ')
        req = urllib.request.Request(f'{FEED}?d1={since}', headers={'User-Agent': 'findcam-refresh'})
        kml = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
    ps = pings(kml)
    if not ps: pm = re.findall(r'<Placemark.*?</Placemark>', kml, re.S); print('no pings in feed', len(kml), 'bytes', len(pm), 'placemarks:', re.sub(r'\s+', ' ', (pm or [kml])[0])[-900:]); return 0
    last_t = ps[-1][0]
    asof = datetime.fromisoformat(D['asof'].replace('Z', '+00:00'))
    if last_t <= asof: print('no new ping since', D['asof']); return 0
    off = -5 if D['lastMile'] >= 2247.5 else -6
    loc = last_t + timedelta(hours=off)
    day_start = (loc.replace(hour=4, minute=0, second=0, microsecond=0) - timedelta(hours=off))
    today = [p for p in ps if p[0] >= day_start]
    if not today: print('no pings today'); return 0
    route = D['route']; prev = D['lastMile']
    new_day = today[0][0] > datetime.fromisoformat(D['firstPing'].replace('Z', '+00:00')) + timedelta(hours=12)
    lo = prev - 3; hi = prev + 90
    first = project(route, today[0][1], today[0][2], lo, hi)
    lastp = project(route, today[-1][1], today[-1][2], lo, hi)
    if not lastp or lastp[0] > 3: print('last ping is off the route, leaving data as is', lastp); return 0
    m = max(round(lastp[1], 1), prev if not new_day else 0)
    if new_day and first and first[0] <= 3:
        D['firstPing'] = today[0][0].strftime('%Y-%m-%dT%H:%M:%SZ'); D['todayStartMile'] = round(first[1], 1)
    D['lastMile'] = m
    D['asof'] = last_t.strftime('%Y-%m-%dT%H:%M:%SZ')
    miles = m - D['todayStartMile']
    D['todayMiles'] = round(miles, 1)
    fp = datetime.fromisoformat(D['firstPing'].replace('Z', '+00:00'))
    if miles > 2: D['todayPace'] = round((last_t - fp).total_seconds() / 60 / miles, 2)
    json.dump(D, open(P, 'w'), separators=(',', ':'))
    print('updated', D['asof'], 'mile', m, 'today', D['todayMiles'], 'pace', D['todayPace'])
    return 0

if __name__ == '__main__':
    sys.exit(main(open(sys.argv[1]).read() if len(sys.argv) > 1 else None))
