import sys
import datetime, time
import pandas as pd
from gettxs_addr import get_txs_addr
import base64
import json
import requests

def datetime_to_timestamp(dt):
    t = dt.timetuple()
    ts = int(time.mktime(t)) - time.timezone
    return ts

if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise ValueError("Missing date value")
    date = sys.argv[1]
    try:
        start_date = datetime.datetime.strptime(date[:8],"%Y%m%d")
        end_date = datetime.datetime.strptime(date[-8:],"%Y%m%d")
    except:
        raise ValueError("Wrong date value")

    names = ["Gate1", "Gate2", "Gate3", "Huobi", "Binance1", "Binance2", "Okex1", "Okex2", "LBank", "BCEX", "ceo.bi", "BBAEX", "AllCoin"]
    addrs = ["n1Wt2VbPAR6TttM17HQXscCyWBrFe36HeYC", "n1Ugq21nif8BQ8uw81SwXHK6DHqeTEmPRhj", "n1ZKXqnRWSBSdrR5eDr6nA2E7BL2dJCEavr", "n1KxWR8ycXg7Kb9CPTtNjTTEpvka269PniB", "n1NCdn2vo1vz2didNfnvxPaAPZbh634CLqM", "n1ctrWK6HZ4dZaDLBNLk9pApGgm8KVAnh4r", "n1M6ca8bB3VZyWBryeDBX42kHV9Q8yGXsSP", "n1Ss9YJxCX6XrtEmwuZ2dd38uRq8WsFMuxi", "n1Je6AWHKtrLEEPXeAe74fCzqqmzLLS49wm", "n1KWv3XujZEqWamhd8Nh3cDHmhhLeZJKQko", "n1bvE3Zs4H8gE1QTD1dCS5Gx4hrfLoRA2oW", "n1NRCR4auPGK8yJ11b3GqhBKe2w1mmUioim", "n1aafQBY9V3HVKCKLwBYJDxrF61RMdJNxAR"]

    addr = "n1EoNsJNXG1tN3z9rvjwPKoBXbJMqAjmESC"
    start_ts = datetime_to_timestamp(start_date)+3600*24*7
    end_ts = datetime_to_timestamp(end_date)+3600*24*7
    txs = get_txs_addr(addr,start_ts,end_ts)
    txs = txs[txs["tx_type"]=="call"]
    
    pledge = pd.DataFrame(columns=["address","nas","nat"])
    nr = pd.DataFrame(columns=["address","nr","nat"])
    for i in txs.index:
        data = base64.b64decode(txs.loc[i,"data"])
        obj = json.loads(data)
        if obj.get("Function") == "triggerPledge" or obj.get("function") == "triggerPledge":
            payload = {"hash": txs.loc[i,"hash"]}
            headers = {"Content-Type": "application/json"}
            res = requests.post("https://mainnet.nebulas.io/v1/user/getEventsByHash", json=payload, headers=headers)
            obj = json.loads(res.content)
            events = obj["result"]["events"]
            for event in events:
                if event["topic"] == "chain.contract.pledge":
                    data = json.loads(event["data"])
                    for item in data["data"]:
                        pledge = pledge.append({"address": item["addr"], "nas": float(item["value"]), "nat": float(item["nat"])}, ignore_index=True)
        elif obj.get("Function") == "triggerNR" or obj.get("function") == "triggerNR":
            payload = {"hash": txs.loc[i,"hash"]}
            headers = {"Content-Type": "application/json"}
            res = requests.post("https://mainnet.nebulas.io/v1/user/getEventsByHash", json=payload, headers=headers)
            obj = json.loads(res.content)
            events = obj["result"]["events"]
            for event in events:
                if event["topic"] == "chain.contract.nr":
                    data = json.loads(event["data"])
                    for item in data["data"]:
                        nr = nr.append({"address": item["addr"], "nr": float(item["score"]), "nat": float(item["nat"])}, ignore_index=True)

    ne = 0
    nne = 0
    nat_e = 0.0
    nat_ne = 0.0
    for i in nr.index:
        addr = nr.loc[i,"address"]
        nat = nr.loc[i,"nat"]
        if addr in addrs:
            ind = addrs.index(addr)
            nat_e += nat
            if nat != 0.0: ne += 1
            nr.loc[i,"affiliation"] = names[ind]
        else:
            if nat != 0.0: nne += 1
            nat_ne += nat
            nr.loc[i,"affiliation"] = ""

    nr = nr.sort_values(by=["nr","address"],ascending=False)
    nr.to_csv("nr_result_"+date+".csv",sep=",",index=False)

    print "Addresses eligible for NAT (NR portion):", len(nr[nr["nat"]!=0.0])
    print "Total NAT issued (NR portion):", sum(nr["nat"])
    print "For exchange addresses:", nat_e
    print "For non-exchange addresses:", nat_ne
    print "Exchange addresses:", ne
    print "Non-exchange addresses:", nne
    print 

    pledge = pledge.sort_values(by=["nas","address"],ascending=False)
    pledge.to_csv("pledge_result_"+date+".csv",sep=",",index=False)

    print "Addresses eligible for NAT (pledge portion):", len(pledge)
    print "Total NAT distributed (pledge portion):", sum(pledge["nat"])
    print "Total NAS eligible for NAT (pledge portion):", sum(pledge["nas"])

