import sys
import datetime
import pandas as pd
from getnr import get_nr_by_week

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
    z = 12.663

    iweek = (start_date-datetime.datetime.strptime("20190506","%Y%m%d")).days/7

    names = ["Gate1", "Gate2", "Gate3", "Huobi", "Binance1", "Binance2", "Okex1", "Okex2", "LBank", "BCEX", "ceo.bi", "BBAEX", "AllCoin"]
    addrs = ["n1Wt2VbPAR6TttM17HQXscCyWBrFe36HeYC", "n1Ugq21nif8BQ8uw81SwXHK6DHqeTEmPRhj", "n1ZKXqnRWSBSdrR5eDr6nA2E7BL2dJCEavr", "n1KxWR8ycXg7Kb9CPTtNjTTEpvka269PniB", "n1NCdn2vo1vz2didNfnvxPaAPZbh634CLqM", "n1ctrWK6HZ4dZaDLBNLk9pApGgm8KVAnh4r", "n1M6ca8bB3VZyWBryeDBX42kHV9Q8yGXsSP", "n1Ss9YJxCX6XrtEmwuZ2dd38uRq8WsFMuxi", "n1Je6AWHKtrLEEPXeAe74fCzqqmzLLS49wm", "n1KWv3XujZEqWamhd8Nh3cDHmhhLeZJKQko", "n1bvE3Zs4H8gE1QTD1dCS5Gx4hrfLoRA2oW", "n1NRCR4auPGK8yJ11b3GqhBKe2w1mmUioim", "n1aafQBY9V3HVKCKLwBYJDxrF61RMdJNxAR"]

    print("Requesting NRs..")

    nrs = get_nr_by_week(date)

    nat = pd.DataFrame(columns=["address", "nr", "nat", "affiliation"])
    nr_e = 0.0
    for i in nrs.index:
        addr = nrs.loc[i,"address"]
        nr = nrs.loc[i,"score"]
        if addr in addrs:
            ind = addrs.index(addr)
            nr_e += nr
            nat = nat.append({"address": addr, "nr": nr, "affiliation": names[ind]}, ignore_index=True)
        else:
            nat = nat.append({"address": addr, "nr": nr}, ignore_index=True)

    nr_tot = sum(nrs["score"])
    nr_ne = nr_tot - nr_e
    print "Total NR:", nr_tot
    print "Sum NR of exchanges:", nr_e
    print "Sum NR of non-exchange addresses:", nr_ne
    print
    #z = 1e11*(1-lam)/((mu+1)*nr_ne+nr_e)

    for i in nat.index:
        nat.loc[i,"nat"] = z*nat.loc[i,"nr"]*lam**iweek
    nat = nat.sort_values(by="nr",ascending=False)
    nat.to_csv("nat_nr_"+date+".csv",sep=",",index=False)
    print "Addresses eligible for NAT (NR portion):", len(nat[nat["nat"]!=0.0])
    print "Total NAT issued (NR portion):", sum(nat["nat"])
    print "For exchange addresses:", z*nr_e*lam**iweek
    print "For non-exchange addresses:", z*nr_ne*lam**iweek

