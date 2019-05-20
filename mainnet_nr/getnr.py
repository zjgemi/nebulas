import httplib
import json
import pandas as pd
import time

def get_nr_by_week(date):

    host = "111.203.228.11:9973"
    conn = httplib.HTTPConnection(host)

    while(True):
        conn.request(method="GET",url="http://"+host+"/keyset?db=nebulas&collection=nr_7&field=date")
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
    if date not in obj["result"]:
        raise ValueError("Date value not in the list")

    while(True):
        conn.request(method="GET",url="http://"+host+"/nr?date="+date+"&db=nebulas&collection=nr_7")
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
        nrs = nrs.append({'address': res["address"], 'score': res["score"]}, ignore_index=True)

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
            nrs = nrs.append({'address': res["address"], 'score': res["score"]}, ignore_index=True)

    return nrs

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
