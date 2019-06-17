# Mainnet NAT

Analyzing the result of NAT distributing on mainnet.

## NR portion

Calculating the result of NAT distributing (NR portion).
An example Python code `nat_nr.py` is provided.
One can run the code by passing a week in the form of `YYYYmmdd-YYYYmmdd` as the commandline argument, e.g.
```bash
python nat_nr.py 20190506-20190513
```

## Pledge portion

Calculating the result of NAT distributing (pledge portion).
An example Python code `nat_pledge.py` is provided.
One can run the code by passing the week of pledge in the form of `YYYYmmdd-YYYYmmdd` as the commandline argument, e.g.
```bash
python nat_pledge.py 20190506-20190513
```

Analyzing the pledge transactions in a time interval.
An example Python code `stat_pledge.py` is provided.
One can run the code by passing the start date and the end date in the form of `YYYYmmdd` as the commandline arguments, e.g.
```bash
python stat_pledge.py 20190527 20190603
```

## Parse results

Parse the onchain results of NAT distributing (NR and pledge portions).
An example Python code `parse_results.py` is provided.
One can run the code by passing a week in the form of `YYYYmmdd-YYYYmmdd` as the commandline argument, e.g.
```bash
python parse_results.py 20190603 20190610
```

