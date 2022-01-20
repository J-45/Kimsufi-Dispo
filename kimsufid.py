#/usr/bin/python3

import re
import json
import time
from urllib import request

SRV_MODEL       = "KS-1"
FREE_USR        = ""
API_KEY         = ""
MAIN_URL        = "https://www.kimsufi.com/fr/serveurs.xml"
JSON_URL        = "https://www.ovh.com/engine/api/dedicated/server/availabilities?country=fr"
MAIN_HTML       = request.urlopen(MAIN_URL).read().decode('utf-8')
DATA_REF        = re.findall("data-ref=\"(\w+)\" [^>]+>\s+<td><[^>]+>"+SRV_MODEL+"<", MAIN_HTML)[0]
last_time       = 0

def send_sms(usr, key, txt):
    DATA        = {'user': usr, 'pass': key, 'msg': txt}
    JSONDATA    = json.dumps(DATA).encode("utf8")
    req         = request.Request("https://smsapi.free-mobile.fr/sendmsg")
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(JSONDATA))
    RES         = request.urlopen(req, JSONDATA)
    PAGE        = RES.read().decode("utf8")
    if RES.getcode() != 200:
        print(RES.getcode())
    return PAGE

while True:
    dispo = False
    try:
        JSON_RESP       = request.urlopen(JSON_URL).read().decode('utf-8')
        STRUCTURED_JSON = json.loads(JSON_RESP)
        for row in STRUCTURED_JSON:
            if row["hardware"] == DATA_REF:
                # print("---------\n", json.dumps(row, indent=2, sort_keys=False)) # Debug
                for range_counter in range( len(row["datacenters"]) ):
                    # REGION         = row["region"] # Debug
                    # DATACENTER     = row["datacenters"][range_counter]["datacenter"] # Debug
                    AVAILABILITY     = row["datacenters"][range_counter]["availability"]
                    if AVAILABILITY != "unavailable":
                        dispo        = True

        if dispo:
            print("( ^ᴗ^ )", end=" ", flush=True)
            ELAPSED_TIME    = time.time() - last_time
            if ELAPSED_TIME > 60*60: # 60*60 secondes
                last_time   = time.time()
                send_sms(FREE_USR, API_KEY, f"Server {SRV_MODEL} dispo !")

        else:
            print("(╥_╥)", end=" ", flush=True)
    except:
        print("╭∩╮ (ò╭╮Ó,)", end=" ", flush=True)
    
    time.sleep(60)
