#!/usr/bin/env bash
# Upload index.html to the FTP account whose home folder is camerondeanbalser.com/run.
# FTP_SERVER may be a host or an IP. For an IP, the TLS certificate's host name is found
# and curl connects to that name at the IP, so the certificate is still verified.
# Never prints the username or password.
set -uo pipefail
S="${FTP_SERVER:-}"; S="${S#*://}"; S="${S%%/*}"; S="$(echo -n "$S" | tr -d '[:space:]')"
if [ -z "$S" ] || [ -z "${FTP_USERNAME:-}" ]; then echo "ftp: settings missing"; exit 2; fi
U="$(echo -n "$FTP_USERNAME" | tr -d '\r\n')"
try() { # $1 url host, $2 extra curl args
  out=$(curl -sS --ssl-reqd --connect-timeout 30 --max-time 120 $2 -T index.html --user "$U:$FTP_PASSWORD" "ftp://$1/index.html" 2>&1); rc=$?
  if [ $rc = 0 ]; then echo "ftp: uploaded index.html via $1"
    curl -sS --ssl-reqd --connect-timeout 30 $2 --list-only --user "$U:$FTP_PASSWORD" "ftp://$1/" 2>/dev/null | head -20 | sed 's/^/ftp: home has: /'
    exit 0; fi
  echo "ftp: attempt via $1 failed: $out" | head -2
}
if [[ $S =~ ^[0-9.]+$ ]]; then
  names=$( { dig +short -x "$S" | sed 's/\.$//';
    echo | timeout 20 openssl s_client -starttls ftp -connect "$S:21" 2>/dev/null | openssl x509 -noout -ext subjectAltName -subject 2>/dev/null | grep -oE '[A-Za-z0-9*.-]+\.[a-z]{2,}' ; } | grep -v '^\*' | sort -u)
  echo "ftp: certificate and reverse DNS names: $(echo $names)"
  for n in $names; do try "$n" "--connect-to $n:21:$S:21"; done
else
  try "$S" ""
fi
exit 1
