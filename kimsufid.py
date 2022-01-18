#/usr/bin/python3

import re
import json
import time
import urllib.request

srv_model       = "KS-1"
main_url        = "https://www.kimsufi.com/fr/serveurs.xml"
json_url        = "https://www.ovh.com/engine/api/dedicated/server/availabilities?country=fr"
main_html       = urllib.request.urlopen(main_url).read().decode('utf-8')
data_ref        = re.findall("data-ref=\"(\w+)\" [^>]+>\s+<td><[^>]+>"+srv_model+"<", main_html)[0]

while True:
    dispo = False
    try:
        json_resp       = urllib.request.urlopen(json_url).read().decode('utf-8')
        structured_json = json.loads(json_resp)
        for row in structured_json:
            if row["hardware"] == data_ref:
                # print("---------\n", json.dumps(row, indent=2, sort_keys=False)) # Debug
                for range_counter in range(0, len(row["datacenters"])):
                    region = row["region"]
                    datacenter = row["datacenters"][range_counter]["datacenter"]
                    availability = row["datacenters"][range_counter]["availability"]
                    if availability != "unavailable":
                        dispo = True

        if dispo:
            print("( ^ᴗ^ )", end=" ", flush=True)
        else:
            print("(╥_╥)", end=" ", flush=True)
    except:
        print("╭∩╮ (ò╭╮Ó,)", end=" ", flush=True)
    
    time.sleep(60)
