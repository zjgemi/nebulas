# Mainnet NR

Tracking NR status of mainnet.

## Plot NR bar chart

Stacked bar chart is plotted for NR proportions of certain selected addresses. Two example Python codes `plot_nr_bar_by_day.py` and `plot_nr_bar_by_week.py` are provided which present the results day by day or week by week, respectively. One can run the codes by passing the start date and end date in the form of `YYYYmmdd` as the commandline arguments, e.g.
```bash
python plot_nr_bar_by_day.py 20190301 20190331
```
or
```bash
python plot_nr_bar_by_week.py 20190301 20190331
```
You can modify the list of selected addresses in the code.

## Plot total tx_value and total NR

Study the variation of total tx_value and total NR. Two example Python codes `plot_tx_val_by_day.py` and `plot_tx_val_by_week.py` are provided which present the results day by day or week by week, respectively. One can run the codes by passing the start date and end date in the form of `YYYYmmdd` as the commandline arguments, e.g.
```bash
python plot_tx_val_by_day.py 20190301 20190331
```
or
```bash
python plot_tx_val_by_week.py 20190301 20190331
```
