import httplib
import json
import pandas as pd
import time
import os

def get_txs_addr(addr,start_ts,end_ts):

    host = "111.203.228.11:9973"
    conn = httplib.HTTPConnection(host)
    period = 3600*24
    
    txs = pd.DataFrame(columns=["tx_type", "from", "to", "tx_value", "timestamp", "data", "hash"])

    from_ts = start_ts
    to_ts = min(end_ts,from_ts+period)
    while(from_ts < to_ts):

        cnt = 0
        while(True):
            conn.request(method="GET",url="http://"+host+"/transaction?db=nebulas&batch_size=100&address="+addr+"&start_ts="+str(from_ts)+"&end_ts="+str(to_ts))
            try:
                response = conn.getresponse()
                res = response.read()
                obj = json.loads(res)
            except:
                print("respose")
                print(response)
                print("res")
                print(res)
                time.sleep(1)
                continue
            break

        cnt += len(obj["result"])
        for res in obj["result"]:
            if res["status"] == 1:
                txs = txs.append({"tx_type": res["tx_type"], "from": res["from"], "to": res["to"], "tx_value": float(res["tx_value"]), "timestamp": res["timestamp"], "data": res["data"], "hash": res["hash"]}, ignore_index=True)
        
        getid = obj["id"]
        while(obj["has_more"]):
            conn.request(method="GET",url="http://"+host+"/cursor?db=nebulas&id="+getid)
            try:
                response = conn.getresponse()
                res = response.read()
                obj = json.loads(res)
            except:
                print("respose")
                print(response)
                print("res")
                print(res)
                time.sleep(1)
                continue
            cnt += len(obj["result"])
            if cnt >= 32768:
                raise ValueError("Number of txs reach the ceiling")
            for res in obj["result"]:
                if res["status"] == 1:
                    txs = txs.append({"tx_type": res["tx_type"], "from": res["from"], "to": res["to"], "tx_value": float(res["tx_value"]), "timestamp": res["timestamp"], "data": res["data"], "hash": res["hash"]}, ignore_index=True)
        
        from_ts = to_ts
        to_ts = min(end_ts,from_ts+period)

    return txs

