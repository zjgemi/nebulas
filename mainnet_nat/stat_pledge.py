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

    if len(sys.argv) < 3:
        raise ValueError("Missing date value")
    start_sdate = sys.argv[1]
    end_sdate = sys.argv[2]
    try:
        start_date = datetime.datetime.strptime(start_sdate,"%Y%m%d")
        end_date = datetime.datetime.strptime(end_sdate,"%Y%m%d")
    except:
        raise ValueError("Wrong date value")

    pledge1 = "n1n5Fctkjx2pA7iLX8rgRyCa7VKinGFNe9H"
    pledge2 = "n1obU14f6Cp4Wv7zANVbtmXKNkpKCqQDgDM"

    print("Requesting txs..")
    nat = pd.DataFrame(columns=["address", "nas", "nat"])
    ntp = 0
    ntr = 0

    start_ts = datetime_to_timestamp(start_date) - 3600*5 + 60*27
    end_ts = datetime_to_timestamp(end_date) - 3600*5 + 60*27
    txs = get_txs_addr(pledge1,start_ts,end_ts)
    txs = txs.sort_values(by="timestamp")
    ind = txs[(txs["to"]=="n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX") & (txs["timestamp"]=="1557710010")].index
    if len(ind) != 0: txs = txs.drop(ind)
    for i in txs.index:
        if (txs.loc[i,"to"] == pledge1) & (txs.loc[i,"tx_type"] == "call") & (txs.loc[i,"tx_value"] != 0.0):
            nas = txs.loc[i,"tx_value"]*1e-18
            addr = txs.loc[i,"from"]
            nat = nat.append({"address": addr, "nas": nas}, ignore_index=True)
            ntp += 1
        elif txs.loc[i,"from"] == pledge1:
            addr = txs.loc[i,"to"]
            ind = nat[nat["address"] == addr].index
            if len(ind) != 0:
                nat = nat.drop(ind)
            ntr += 1

    start_ts = datetime_to_timestamp(start_date) - 3600*5 + 60*27
    end_ts = datetime_to_timestamp(end_date) - 3600*5 + 60*27
    txs = get_txs_addr(pledge2,start_ts,end_ts)
    txs = txs.sort_values(by="timestamp")
    ind = txs[(txs["from"]=="n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX") & (txs["timestamp"]=="1557712830")].index
    if len(ind) != 0: txs = txs.drop(ind)
    for i in txs.index:
        if (txs.loc[i,"to"] == pledge2) & (txs.loc[i,"tx_type"] == "call") & (txs.loc[i,"tx_value"] != 0.0):
            if txs.loc[i,"from"] == "n1LEdnBHdhZYaacnCmmiWRKvgPAiCdPZUsX":
                print txs.loc[i]
            nas = txs.loc[i,"tx_value"]*1e-18
            addr = txs.loc[i,"from"]
            nat = nat.append({"address": addr, "nas": nas}, ignore_index=True)
            ntp += 1
        elif txs.loc[i,"from"] == pledge2:
            addr = txs.loc[i,"to"]
            ind = nat[nat["address"] == addr].index
            if len(ind) != 0:
                nat = nat.drop(ind)
            ntr += 1

    print "Total transactions in this interval:", ntp + ntr
    print "Pledge transactions in this interval:", ntp
    print "Redeeming transactions in this interval:", ntr
    print "New pledge NAS:", sum(nat["nas"])
    print "New addresses pledged:", len(nat)

