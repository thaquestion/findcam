#!/usr/bin/env bash
# Keeps findcam fresh: every 5 minutes from about 5am to 10pm in Cam's time zone
# (10:00 to 03:59 UTC) it reads his Garmin feed, rebuilds the page, pushes it to
# GitHub Pages and uploads it to camerondeanbalser.com/run. One run lasts about
# 5.5 hours, then starts the next run, so it never depends on GitHub's cron.
set -uo pipefail
git config user.name "findcam-bot"
git config user.email "findcam-bot@users.noreply.github.com"
END=$((SECONDS + 5*3600 + 30*60))
uploaded=""
upload() {
  if [ -z "${FTP_SERVER:-}" ] || [ -z "${FTP_USERNAME:-}" ]; then echo "ftp: secrets missing, skipped"; return; fi
  sum=$(sha1sum index.html | cut -c1-40)
  [ "$sum" = "$uploaded" ] && return
  if curl -sS --ssl --connect-timeout 30 --max-time 120 -T index.html --user "$FTP_USERNAME:$FTP_PASSWORD" "ftp://$FTP_SERVER/index.html"; then
    uploaded=$sum; echo "ftp: uploaded index.html"
  else echo "ftp: upload failed"; fi
}
while :; do
  h=$((10#$(date -u +%H)))
  if [ "${FORCE_ONCE:-0}" = 1 ] || [ $h -ge 10 ] || [ $h -lt 4 ]; then
    git pull -q --rebase origin main || git rebase --abort
    python build/live.py || echo "live.py failed"
    python build/page.py && cp build/meet-cam.html index.html
    git add build/data.json index.html
    if ! git diff --cached --quiet; then
      git commit -qm "Refresh Cam's position" && (git push -q origin HEAD:main || (git pull -q --rebase origin main && git push -q origin HEAD:main)) && echo "pushed"
    fi
    upload
    FORCE_ONCE=0
  fi
  [ $SECONDS -ge $END ] && break
  [ "${ONE_SHOT:-0}" = 1 ] && exit 0
  sleep 300
done
echo "starting the next run"
gh api -X POST "repos/$GITHUB_REPOSITORY/actions/workflows/refresh.yml/dispatches" -f ref=main
