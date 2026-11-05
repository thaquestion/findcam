#!/usr/bin/env bash
# Print public DNS for Cam's domain and which hosts answer on FTP port 21.
D=camerondeanbalser.com
for t in A NS MX TXT; do echo "== $t $D"; dig +short $t $D; done
for n in www ftp mail webmail cpanel; do echo "== A $n.$D"; dig +short A $n.$D; echo "   CNAME: $(dig +short CNAME $n.$D)"; done
cands=$( (dig +short A $D; for n in ftp mail webmail cpanel; do dig +short A $n.$D; done; dig +short MX $D | awk '{print $2}'; dig +short TXT $D | grep -o 'ip4:[0-9./]*' | cut -d: -f2 | cut -d/ -f1) | grep -v '^$' | sort -u)
echo "== port 21 checks"
for c in $cands; do
  if timeout 8 bash -c "exec 3<>/dev/tcp/${c%.}/21 && head -c 200 <&3" 2>/dev/null | head -1 > /tmp/b; then echo "OPEN $c :: $(tr -d '\r' </tmp/b)"; else echo "closed $c"; fi
done
