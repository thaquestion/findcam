"""Put the tracker dashboard's measured route for Cam's day onto the page.
Usage: python build/splice_today.py <today.csv>
today.csv is the dashboard's "today" dataset (kind=route rows: course mile, lat, lon).
The page's own course past Iowa is straight lines between towns, which overcounts or
loses pings on winding roads. This swaps in the measured line for that day's stretch,
lined up to the page's mile scale where the measured line starts. Touches route, and pulls lastMile back if the old line overcounted."""
import csv, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'data.json')
def hav(a, b, c, d):
    r = math.radians; x = math.sin(r(c-a)/2)**2 + math.cos(r(a))*math.cos(r(c))*math.sin(r(d-b)/2)**2
    return 7917.6*math.asin(math.sqrt(x))
def main(path):
    rows = list(csv.DictReader(open(path)))
    rt = [(float(r['m']), float(r['lat']), float(r['lon'])) for r in rows if r.get('kind') == 'route']
    if len(rt) < 20: print('NO_ROUTE'); return 3
    D = json.load(open(P)); R = D['route']
    # where does the measured line start on the page's scale? nearest page point near his position
    m0, a0, o0 = rt[0]; best = None
    for i in range(len(R)-1):
        m1, a1, o1 = R[i]; m2, a2, o2 = R[i+1]
        if m2 < D['lastMile']-90 or m1 > D['lastMile']+90: continue
        for k in range(11):
            f = k/10; d = hav(a0, o0, a1+f*(a2-a1), o1+f*(o2-o1))
            if best is None or d < best[0]: best = (d, m1+f*(m2-m1))
    if not best or best[0] > 2: print('START_NOT_FOUND', best); return 2
    off = best[1] - m0
    new = [[round(m+off, 2), a, o] for m, a, o in rt]
    lo, hi = new[0][0], new[-1][0]
    old = [p for p in R if lo <= p[0] <= hi]
    if old and len(old) >= len(new) - 2 and abs(old[-1][1]-new[-1][1]) < 1e-4: print('NO_CHANGE'); return 3
    D['route'] = [p for p in R if p[0] < lo] + new + [p for p in R if p[0] > hi]
    # The live refresh never moves lastMile backward, so pull it back to the newest
    # measured ping of today when the old line had counted him too far along.
    from datetime import datetime
    ts = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
    tr = [(ts(r['t']), float(r['m'])+off) for r in rows if r.get('kind') == 'track' and r.get('t')]
    tr = [x for x in tr if x[0] >= ts(D['firstPing']) and lo-1 <= x[1] <= hi+1]
    if tr:
        t, m = max(tr)
        if m < D['lastMile']:
            D['lastMile'] = round(m, 1); D['asof'] = t.strftime('%Y-%m-%dT%H:%M:%SZ')
            D['todayMiles'] = round(D['lastMile']-D['todayStartMile'], 1)
            if D['todayMiles'] > 0: D['todayPace'] = round((t-ts(D['firstPing'])).total_seconds()/60/D['todayMiles'], 2)
            print('RESET_LAST', D['lastMile'], D['asof'])
    json.dump(D, open(P, 'w'), separators=(',', ':'))
    print('SPLICED', lo, hi, 'offset', round(off, 2), 'start match', round(best[0], 2), 'mi'); return 0
if __name__ == '__main__': sys.exit(main(sys.argv[1]))
