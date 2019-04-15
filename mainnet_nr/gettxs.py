import httplib
import json
import pandas as pd

def get_txs(start_ts,end_ts):

    host = "111.203.228.11:9973"
    conn = httplib.HTTPConnection(host)

    while(True):
        conn.request(method="GET",url="http://"+host+"/transaction?db=nebulas&batch_size=100&start_ts="+str(start_ts)+"&end_ts="+str(end_ts))
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
    
    txs = pd.DataFrame(columns=["tx_type", "from", "to", "tx_value"])

    for res in obj["result"]:
        if res["status"] == 1:
            txs = txs.append({"tx_type": res["tx_type"], "from": res["from"], "to": res["to"], "tx_value": float(res["tx_value"])}, ignore_index=True)
    
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
        for res in obj["result"]:
            if res["status"] == 1:
                txs = txs.append({"tx_type": res["tx_type"], "from": res["from"], "to": res["to"], "tx_value": float(res["tx_value"])}, ignore_index=True)

    return txs

