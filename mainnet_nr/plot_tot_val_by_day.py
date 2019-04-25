import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime, time
import pandas as pd
from getnr import get_nr_by_day
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
    
    dates = []
    totval = pd.DataFrame(columns=["date","nr","txval"])
    print("Requesting NRs & txs..")
    date = start_date
    while date <= end_date:
        sdate = date.strftime("%Y%m%d")
        print(sdate)
        nrs = get_nr_by_day(sdate)
        totnr = sum(nrs["score"])

        start_ts = datetime_to_timestamp(date)
        end_ts = datetime_to_timestamp(date+datetime.timedelta(days=1))
        txs = get_txs(start_ts,end_ts)
        txval = sum(txs["tx_value"])
        totval = totval.append({"date": sdate, "nr": totnr, "txval": txval}, ignore_index=True)
        
        dates.append(date)
        date += datetime.timedelta(days=1)
    
    print("Ploting..")
    plt.plot(dates, totval['nr'], color='#000000', label='Total NR')
    plt.legend(loc='upper left')
    plt.xlabel('Date')
    plt.ylabel('Total NR')
    plt.yscale('log')
    ax2 = plt.twinx()
    ax2.plot(dates, totval['txval'], color='#FF0000', label='Total transaction value')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Total transaction value')
    ax2.set_yscale('log')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%y%m%d'))
    plt.savefig('tot_val_'+start_sdate+"_"+end_sdate+'.png')
    plt.close()

    totval.to_csv("tot_val_"+start_sdate+"_"+end_sdate+".csv",sep=",",index=False)
