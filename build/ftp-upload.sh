#!/usr/bin/env bash
# Upload index.html to the FTP account whose home folder is camerondeanbalser.com/run.
# Accepts FTP_SERVER as a bare host, host:port or ftp://host/. Never prints the secrets.
set -uo pipefail
S="${FTP_SERVER:-}"; S="${S#*://}"; S="${S%%/*}"; S="$(echo -n "$S" | tr -d '[:space:]')"
if [ -z "$S" ] || [ -z "${FTP_USERNAME:-}" ]; then echo "ftp: secrets missing"; exit 2; fi
echo "ftp: server value is ${#S} characters, has a dot: $([[ $S == *.* ]] && echo yes || echo no), has a port: $([[ $S == *:* ]] && echo yes || echo no)"
U="$(echo -n "$FTP_USERNAME" | tr -d '\r\n')"
for host in "$S" "ftp.camerondeanbalser.com" "camerondeanbalser.com"; do
  out=$(curl -sS --ssl --connect-timeout 30 --max-time 120 -T index.html --user "$U:$FTP_PASSWORD" "ftp://$host/index.html" 2>&1); rc=$?
  if [ $rc = 0 ]; then echo "ftp: uploaded index.html via $([ "$host" = "$S" ] && echo 'the saved server' || echo "$host")"; exit 0; fi
  echo "ftp: attempt failed ($([ "$host" = "$S" ] && echo 'saved server' || echo "$host")): ${out//$S/<server>}"
done
exit 1
