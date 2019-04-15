import datetime, time
import numpy as np
import pandas as pd
import sys
from getnr import get_nr_by_week
from gettxs import get_txs

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
    
    start_ts = datetime_to_timestamp(start_date)
    end_ts = datetime_to_timestamp(end_date)
    
    print("Requesting NRs..")
    nrs = get_nr_by_week(date)
    print("Requesting transactions..")
    txs = get_txs(start_ts,end_ts)
    calls = txs[txs["tx_type"]=="call"]
    
    print("Calculating DIP result..")
    contracts = set(calls['to'])
    
    edges = pd.DataFrame(columns=["from", "to", "times"])
    addrs = pd.DataFrame(columns=["address", "nr", "times"])
    for ctr in contracts:
        tos = calls[calls['to'] == ctr]
        froms = set(tos['from'])
        for addr in froms:
            times = len(tos[tos['from']==addr])
    
            edges = edges.append({'from': addr, 'to': ctr, 'times': times}, ignore_index=True)
    
            ind = addrs[addrs['address']==addr].index
            if len(ind) == 0:
                resnr = nrs[nrs['address']==addr].index
                if len(resnr) == 0:
                    addrs = addrs.append({'address': addr, 'nr': 0.0, 'times': times}, ignore_index=True)
                else:
                    addrs = addrs.append({'address': addr, 'nr': nrs.loc[resnr[0],'score'], 'times': times}, ignore_index=True)
            else:
                addrs.loc[ind[0],'times'] += times
    
    ctrs = pd.DataFrame(columns=["contract", "score", "reward"])
    for ctr in contracts:
        score = 0.0
        ind = edges[edges['to']==ctr].index
        for j in ind:
            ii = addrs[addrs['address']==edges.loc[j,'from']].index[0]
            score += np.sqrt(addrs.loc[ii,'nr']**2*edges.loc[j,'times']/addrs.loc[ii,'times'])
        ctrs = ctrs.append({'contract': ctr, 'score': score, 'reward': 0.0}, ignore_index=True)
    
    gp = sum(addrs['nr']**2)
    gs = sum(nrs['score']**2)
    lam = min(0.008/(1.0-gp/gs),1.0)
    pool = 19320.0*lam
    
    sums2 = sum(ctrs['score']**2)
    
    for i in ctrs.index:
        ctrs.loc[i,'reward'] = ctrs.loc[i,'score']**2/sums2*pool
    
    ctrs = ctrs.sort_values(by="score",ascending=False)
    ctrs.to_csv("score_"+date+".csv",sep=",",index=False)
    
