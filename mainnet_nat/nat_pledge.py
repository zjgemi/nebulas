import sys
import datetime, time
import pandas as pd
import numpy as np
from gettxs_addr import get_txs_addr

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

    lam = 0.997
    mu = 10.0
    alpha = 5.0
    z = 12.663

    iweek = (start_date-datetime.datetime.strptime("20190506","%Y%m%d")).days/7
    
    pledge1 = "n1n5Fctkjx2pA7iLX8rgRyCa7VKinGFNe9H"
    pledge2 = "n1obU14f6Cp4Wv7zANVbtmXKNkpKCqQDgDM"

    print("Requesting txs..")
    nat = pd.DataFrame(columns=["address", "nas", "nat"])

    start_ts = datetime_to_timestamp(datetime.datetime.strptime("20190504","%Y%m%d"))
    end_ts = datetime_to_timestamp(start_date) - 3600*5 + 60*27
    txs = get_txs_addr(pledge1,start_ts,end_ts)
    txs = txs.sort_values(by="timestamp")
    ind = txs[(txs["to"]=="n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX") & (txs["timestamp"]=="1557710010")].index
    if len(ind) != 0: txs = txs.drop(ind)
    for i in txs.index:
        if (txs.loc[i,"to"] == pledge1) & (txs.loc[i,"tx_type"] == "call") & (txs.loc[i,"tx_value"] != 0.0):
            nas = txs.loc[i,"tx_value"]*1e-18
            addr = txs.loc[i,"from"]
            nat = nat.append({"address": addr, "nas": nas}, ignore_index=True)
        elif txs.loc[i,"from"] == pledge1:
            addr = txs.loc[i,"to"]
            ind = nat[nat["address"] == addr].index
            if len(ind) != 0:
                nat = nat.drop(ind)

    start_ts = datetime_to_timestamp(datetime.datetime.strptime("20190513","%Y%m%d"))
    end_ts = datetime_to_timestamp(start_date) - 3600*5 + 60*27
    txs = get_txs_addr(pledge2,start_ts,end_ts)
    txs = txs.sort_values(by="timestamp")
    ind = txs[(txs["from"]=="n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX") & (txs["timestamp"]=="1557712830")].index
    if len(ind) != 0: txs = txs.drop(ind)
    for i in txs.index:
        if (txs.loc[i,"to"] == pledge2) & (txs.loc[i,"tx_type"] == "call") & (txs.loc[i,"tx_value"] != 0.0):
            nas = txs.loc[i,"tx_value"]*1e-18
            addr = txs.loc[i,"from"]
            nat = nat.append({"address": addr, "nas": nas}, ignore_index=True)
        elif txs.loc[i,"from"] == pledge2:
            addr = txs.loc[i,"to"]
            ind = nat[nat["address"] == addr].index
            if len(ind) != 0:
                nat = nat.drop(ind)

    start_ts = datetime_to_timestamp(start_date) - 3600*5 + 60*27
    end_ts = datetime_to_timestamp(end_date) - 3600*5 + 60*27
    txs2 = get_txs_addr(pledge1,start_ts,end_ts)
    txs2 = txs2.sort_values(by="timestamp")
    ind = txs2[(txs2["to"]=="n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX") & (txs2["timestamp"]=="1557710010")].index
    if len(ind) != 0: txs2 = txs2.drop(ind)
    for i in txs2.index:
        if txs2.loc[i,"from"] == pledge1:
            addr = txs2.loc[i,"to"]
            ind = nat[nat["address"] == addr].index
            if len(ind) != 0:
                nat = nat.drop(ind)

    start_ts = datetime_to_timestamp(start_date) - 3600*5 + 60*27
    end_ts = datetime_to_timestamp(end_date) - 3600*5 + 60*27
    txs2 = get_txs_addr(pledge2,start_ts,end_ts)
    txs2 = txs2.sort_values(by="timestamp")
    ind = txs2[(txs2["from"]=="n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX") & (txs2["timestamp"]=="1557712830")].index
    if len(ind) != 0: txs2 = txs2.drop(ind)
    for i in txs2.index:
        if txs2.loc[i,"from"] == pledge2:
            addr = txs2.loc[i,"to"]
            ind = nat[nat["address"] == addr].index
            if len(ind) != 0:
                nat = nat.drop(ind)

    for i in nat.index:
        nas = nat.loc[i,"nas"]
        nat.loc[i,"nat"] = alpha*z*nas/(1+np.sqrt(200.0/nas))*lam**iweek

    nat = nat.sort_values(by=["nat","address"],ascending=False)
    nat.to_csv("nat_pledge_"+date+".csv",sep=",",index=False)
    print "Addresses eligible for NAT (pledge portion):", len(nat)
    print "Total NAT distributed (pledge portion):", sum(nat["nat"])
    print "Total NAS eligible for NAT (pledge portion):", sum(nat["nas"])

