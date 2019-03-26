# Mainnet DIP
Calculate DIP results in history for mainnet.
An example Python code `dip.py` is provided. One can run the code by passing the date interval in the form of `YYYYmmdd-YYYYmmdd` as the commandline argument, e.g.
```bash
python dip.py 20190311-20190318
```
The list of available date intervals can be found from the API `http://111.203.228.11:9973/keyset?db=nebulas&collection=nr_week&field=date`.
