import sys
import datetime
from collections import Counter
import re

# Extension list using sinfo -o "%P %G %D %N"
partitions = [
    "cpu-long",
    "cpu-short",
    "cpu-preemptable",
    "gpu-2080ti",
    "gpu-2080ti-long",
    "gpu-2080ti-dev",
    "gpu-2080ti-preemptable",
    "gpu-v100",
    "gpu-v100-preemptable",
    "gpu-2080ti-interactive",
    "bethge", "lensch", "macke", "geiger-test"
]
acc_parts = ["bethge", "lensch", "macke", "geiger-test"]
other_parts = ["DOWN","DRAINED","RESERVED"]

all_queues = []
defs = [
    "jobId",
    "state",
    "cpus",
    "nodes",
    "remainTime",
    "reason",
    "account",
    "user",
    "partitions",
]
for ix, line in enumerate(sys.stdin):
    temp_dict = {}
    out_vals = line.strip().split("|")
    new_o_line = []
    temp_list = []
    for idx, line1 in enumerate(out_vals):
        if "," in line1:
            if re.search(r"\b job are DOWN, DRAINED or \b", line1):
                new_o_line.append("UNKNW")
            else:
                new_out_vals = line1.split(",")
                for val in new_out_vals:
                    if val in partitions and val not in temp_list:
                        temp_list.append(val)
        elif idx == 1 and line1 in partitions:
            temp_list.append(line1)
        else:
            new_o_line.append(line1)

    new_o_line.append(temp_list)

    for defi, item in zip(defs, new_o_line):
        if isinstance(item, str):
            item = item.replace(" ", "")
            item = item.replace("\n", "")
            item = item.replace("(", "")
            item = item.replace(")", "")
        temp_dict[defi] = item

    # Obtain Keys
    temp_keys = list(temp_dict.keys())
    for partition in temp_dict['partitions']:
        new_temp = {}
        for key in temp_keys[:-1]:
            new_temp[key] = temp_dict[key]
            new_temp['partition'] = '"' + partition + '"'
        all_queues.append(new_temp)

pp_reservations = {}

for queue in all_queues:
    if queue["partition"] not in pp_reservations:
        pp_reservations[queue["partition"]] = 1
    else:
        pp_reservations[queue["partition"]] += 1


for k, v in pp_reservations.items():
    print(f"jobs_waiting,partition={str(k)} count={int(v)}")


pp_reasons = {}
for queue in all_queues:
    if queue["partition"] not in pp_reasons:
        pp_reasons[queue["partition"]] = {queue["reason"]: 1}
    elif queue["reason"] not in pp_reasons[queue["partition"]]:
        temp_dict = pp_reasons[queue["partition"]]
        temp_dict[queue["reason"]] = 1
        pp_reasons[queue["partition"]] = temp_dict 
    else:
        pp_reasons[queue["partition"]][queue["reason"]] += 1

for k, v in pp_reasons.items():
    for k1,v1 in v.items():
        print(f"jobs_waiting_reasons,reason={k1},partition={k} count={int(v1)}")
