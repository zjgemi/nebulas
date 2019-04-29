import sys
import datetime, time
import pandas as pd
from gettxs import get_txs

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
    
    addrs = pd.DataFrame(columns=["addr","txs","totval"])
    print("Requesting txs..")
    start_ts = datetime_to_timestamp(start_date)
    end_ts = datetime_to_timestamp(end_date+datetime.timedelta(days=1))
    txs = get_txs(start_ts,end_ts)
    all_addrs = set(list(txs['from'])+list(txs['to']))

    for addr in all_addrs:
        sel = txs[(txs['from']==addr) | (txs['to']==addr)]
        times = len(sel)
        totval = sum(sel["tx_value"])
        addrs = addrs.append({"addr": addr, "txs": times, "totval": totval}, ignore_index=True)
    
    addrs = addrs.sort_values(by="totval",ascending=False)
    addrs.to_csv("addrs_txs_"+start_sdate+"_"+end_sdate+".csv",sep=",",index=False)
