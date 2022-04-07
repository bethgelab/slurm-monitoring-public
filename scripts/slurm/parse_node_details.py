import sys
import datetime


all_nodes = []
defs = [
    "host",
    "state",
    "cpu_load",
    "avail_mem",
    "alloc_mem",
    "features"
]

for line in sys.stdin:
    temp_dict = {}
    out_vals = line.split(",")
    for defi, val in zip(defs, out_vals):
        val = val.replace(" ", "")
        val = val.replace("\n", "")
        if not val.isdecimal():
            temp_dict[defi] = '"'+val+'"'
        else:
            temp_dict[defi] = val
    all_nodes.append(temp_dict)

for item in all_nodes:
    values = [f"{k}={item[k]}" for k in item.keys()]
    print(f"node_details,node_host={item['host']} {','.join(values)}")
