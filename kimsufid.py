#/usr/bin/python3

import json
import re
import urllib.request

def get(url):
    with urllib.request.urlopen(main_url) as r:
        return r.read().decode('utf-8')

server_model    = "KS-1"
data_ref        = ""
main_url        = "https://www.kimsufi.com/fr/serveurs.xml"
json_url        = "https://www.ovh.com/engine/api/dedicated/server/availabilities?country=fr"

main_html       = get(main_url)
data_ref        = re.findall("data-ref=\"(\w+)\" [^>]+>\s+<td><[^>]+>KS-1<", main_html)[0]
json_resp       = get(json_url)
j               = json.loads(json_resp)

for row in j:
    if row["hardware"] == data_ref:
        print(json.dumps(row, indent=2, sort_keys=True))