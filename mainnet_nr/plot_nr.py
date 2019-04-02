import httplib
import json
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pandas as pd

def get_nr_by_day(date):

    host = "111.203.228.11:9973"
    conn = httplib.HTTPConnection(host)

    while(True):
        conn.request(method="GET",url="http://"+host+"/nr?db=nebulas&date="+date)
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

    nrs = pd.DataFrame(columns=["address", "score"])

    for res in obj["result"]:
        nrs = nrs.append({"address": res["address"], "score": res["score"]}, ignore_index=True)

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
            nrs = nrs.append({"address": res["address"], "score": res["score"]}, ignore_index=True)

    return nrs

if __name__ == "__main__":

    if len(sys.argv) < 3:
        raise ValueError("Missing date value")
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    try:
        date = datetime.datetime.strptime(start_date,"%Y%m%d")
        enddate = datetime.datetime.strptime(end_date,"%Y%m%d")
    except:
        raise ValueError("Wrong date value")

    names = ["Gate1", "Gate2", "Gate3", "Huobi", "Binance1", "Binance2", "Okex1", "Okex2", "LBank", "BCEX", "ceo.bi", "BBAEX", "AllCoin", "large1", "large2", "large3", "large4"]
    addrs = ["n1Wt2VbPAR6TttM17HQXscCyWBrFe36HeYC", "n1Ugq21nif8BQ8uw81SwXHK6DHqeTEmPRhj", "n1ZKXqnRWSBSdrR5eDr6nA2E7BL2dJCEavr", "n1KxWR8ycXg7Kb9CPTtNjTTEpvka269PniB", "n1NCdn2vo1vz2didNfnvxPaAPZbh634CLqM", "n1ctrWK6HZ4dZaDLBNLk9pApGgm8KVAnh4r", "n1M6ca8bB3VZyWBryeDBX42kHV9Q8yGXsSP", "n1Ss9YJxCX6XrtEmwuZ2dd38uRq8WsFMuxi", "n1Je6AWHKtrLEEPXeAe74fCzqqmzLLS49wm", "n1KWv3XujZEqWamhd8Nh3cDHmhhLeZJKQko", "n1bvE3Zs4H8gE1QTD1dCS5Gx4hrfLoRA2oW", "n1NRCR4auPGK8yJ11b3GqhBKe2w1mmUioim", "n1aafQBY9V3HVKCKLwBYJDxrF61RMdJNxAR", "n1F3W6La7gtKrZa5D5qpEdzLhkwf7k4YSg3", "n1HqgHgKh1iQ7GbSGycVhK7LRa1eNScN1i2", "n1Ex2onGzKn38cAgJxoAzrzXkwLYAVrTRV7", "n1FgV3qzWXgkdqMtE9YhnnGYmci5P1CETkc"]
    
    ratio = pd.DataFrame(columns=["date"]+names+["totnr"])
    dates = []
    print("Requesting NRs..")
    while date <= enddate:
        sdate = date.strftime("%Y%m%d")
        print(sdate)
        ratio = ratio.append({"date": sdate}, ignore_index=True)
        i = ratio[ratio["date"] == sdate].index[0]
        nrs = get_nr_by_day(sdate)
        for name, addr in zip(names,addrs):
            ind = nrs[nrs["address"]==addr].index
            if(ind.size == 0):
                nr = 0.0
            else:
                nr = nrs.loc[ind[0],"score"]
            ratio.loc[i,name] = nr
        totnr = sum(nrs["score"])
        ratio.loc[i,"totnr"] = totnr
        dates.append(date)
        date += datetime.timedelta(days=1)
    
    print("Ploting..")
    bottom = [0.0]*len(ratio)
    for name in names:
        plt.bar(dates, ratio[name]/ratio["totnr"], bottom=bottom, label=name)
        bottom += ratio[name]/ratio["totnr"]
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.8 , box.height])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m%d"))
    plt.xlabel("Date")
    plt.ylabel("NR ratio")
    plt.savefig("NR_"+start_date+"_"+end_date+".png")
    plt.close()

    ratio.to_csv("ratio_"+start_date+"_"+end_date+".csv",sep=",",index=False)
