import sys
import datetime

item_keys = ["type","resource","usage"]
all_qinfos = []
for line in sys.stdin:
    out_list = line.strip().split(",")
    cleaned_list = []
    temp_dict = {}
    for item in out_list:
        item = item.replace(" ", "")
        item = item.replace(":","")
        item = item.replace("(","")
        item = item.replace(")","")
        item = item.replace("\n","")
        item = item.replace("%","")
        cleaned_list.append(item)
    for item_key, item in zip(item_keys, cleaned_list):
        if item.isdecimal():
            temp_dict[item_key] = int(item)
        else:
            temp_dict[item_key] = item
    all_qinfos.append(temp_dict)

for qinfo in all_qinfos:
    values = []
    for k in qinfo.keys():
        if isinstance(qinfo[k], str):
            value = '"' + qinfo[k] + '"'
            values.append(f"{k}={value}")
        else:
            values.append(f"{k}={qinfo[k]}")
    print(f"qinfo_quota,measure={qinfo['resource']} {','.join(values)}")