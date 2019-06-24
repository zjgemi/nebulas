import sys
import datetime, time
import pandas as pd
from gettxs_addr import get_txs_addr
import base64
import json
import requests
import os

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

    mu = 10.0

    filename = "nat_voting_"+date+".csv"
    if(os.path.exists(filename)):
        nat = pd.read_csv(filename)
    else:
        
        vote = "n1pADU7jnrvpPzcWusGkaizZoWgUywMRGMY"

        print("Requesting txs..")
        start_ts = datetime_to_timestamp(start_date) + 3600*4
        end_ts = datetime_to_timestamp(end_date) + 3600*4
        txs = get_txs_addr(vote,start_ts,end_ts)
        txs = txs.sort_values(by="timestamp")
        nat = pd.DataFrame(columns=["address", "vote", "nat"])

        cnt = 0
        for i in txs.index:
            cnt += 1
            data = base64.b64decode(txs.loc[i,"data"])
            obj = json.loads(data)
            if obj.get("Function") == "vote":
                addr = txs.loc[i,"from"]
                args = json.loads(obj["Args"])
                amount = float(args[3])*1e-18

                payload = {"hash": txs.loc[i,"hash"]}
                headers = {"Content-Type": "application/json"}
                res = requests.post("https://mainnet.nebulas.io/v1/user/getEventsByHash", json=payload, headers=headers)
                obj = json.loads(res.content)
                events = obj["result"]["events"]
                reward = 0.0
                for event in events:
                    if event["topic"] == "chain.contract.vote":
                        data = json.loads(event["data"])
                        if type(data) == dict:
                            reward = float(data.get("reward"))

                ind = nat[nat["address"]==addr].index
                if len(ind) == 0:
                    nat = nat.append({"address": addr, "vote": amount, "nat": reward}, ignore_index=True)
                else:
                    nat.loc[ind[0],"vote"] += amount
                    nat.loc[ind[0],"nat"] += reward
                print cnt, "of", len(txs), ":", addr, amount, reward

        nat = nat.sort_values(by=["vote","address"],ascending=False)
        nat.to_csv(filename,sep=",",index=False)

    print "Total NAT issued (voting portion):", sum(nat["nat"])
    print "Total NAT used for voting:", sum(nat["vote"])
    print "NAT used for voting with reward:", sum(nat["nat"])/mu
    print "NAT used for voting without reward:", sum(nat["vote"]) - sum(nat["nat"])/mu
    print "Voters with reward:", len(nat[nat["nat"]!=0.0])
    print "Voters without reward:", len(nat[nat["vote"]!=0.0]) - len(nat[nat["nat"]!=0.0])

