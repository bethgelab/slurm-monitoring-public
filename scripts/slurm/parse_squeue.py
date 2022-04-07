import sys
import datetime
from collections import Counter

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
for line in sys.stdin:
    temp_dict = {}
    out_vals = line.split(",")

    new_o_line = []
    temp_list = []
    for idx, line in enumerate(out_vals):
        if line in partitions and line not in temp_list:
            if idx != 1 and line in acc_parts:
                new_o_line.append(line)
            else:
                temp_list.append(line)
        else:
            new_o_line.append(line)

    new_o_line.append(temp_list)

    for defi, val in zip(defs, new_o_line):
        if isinstance(val, str):
            val = val.replace(" ", "")
            val = val.replace("\n", "")
            val = val.replace("(", "")
            val = val.replace(")", "")
        #val = val.replace("-", "")
        #val = val.replace("_", "")
        temp_dict[defi] = val

    # Obtain Keys
    temp_keys = list(temp_dict.keys())
    for partition in temp_dict['partitions']:
        new_temp = {}
        for key in temp_keys[:-1]:
            new_temp[key] = temp_dict[key]
            new_temp['partition'] = partition
        all_queues.append(new_temp)

account_dict = {}
for queue in all_queues:
    if queue["account"] not in account_dict:
        account_dict[queue["account"]] = 1
    else:
        account_dict[queue["account"]] += 1

for item in all_queues:
    values = []
    #values = [f"{k}={item[k]}" for k in item.keys()]
    for k in item.keys():
        if k == "remainTime":
            if "-" in item["remainTime"]:
                sub_set = item["remainTime"].split("-")
                values.append("days=" + sub_set[0])
                hms = sub_set[1].split(":")
            else:
                hms = item["remainTime"].split(":")
            setting = ["h", "m", "s"]
            for idx, vals in enumerate(hms):
                if vals == "UNLIMITED":
                    values.append(f"{setting[idx]}=999")
                elif vals.isdecimal():
                    values.append(f"{setting[idx]}={vals}")
                else:
                    vals = '"' + vals + '"'
                    values.append(f"{setting[idx]}={vals}")
        else:
            if not item[k].isdecimal():
                val = item[k].lower()
                val = '"' + val + '"'
                values.append(f"{k}={val}")
            else:
                values.append(f"{k}={item[k]}")

    print(
        f"squeue,job={item['jobId']},user={item['user']},partition={item['partition']} {','.join(values)}")

for item in all_queues:
    values = []
    s = 0
    if "-" in item["remainTime"]:
        sub_set = item["remainTime"].split("-")
        s += int(sub_set[0]) * 86400
        # values.append("days=" + sub_set[0])
        hms = sub_set[1].split(":")
    else:
        hms = item["remainTime"].split(":")
    setting = ["h", "m", "s"]
    for idx, vals in enumerate(hms):
        if vals == "UNLIMITED":
            # Total time is an arbitary number
            values.append(f"job_rtime=-9999")
            break
        elif vals.isdecimal():
            if idx == 0:
                s += int(vals) * 3600
            elif idx == 1:
                s += int(vals) * 60
            else:
                s += int(vals)
    # Hour remain for the job
    h = s * 0.000277778
    values.append(f"job_rtime={h}")
    print(
        f"squeueUtime,userId={item['user']},jobId={item['jobId']} {','.join(values)}"
    )

for k, v in account_dict.items():
    print(
        f"squeueAccount,accName={str(k)} count={str(v)}")

user_dict = {}
for queue in all_queues:
    if queue["user"] not in user_dict or queue["state"] not in user_dict[queue["user"]]:
        if queue["state"] == "RUNNING":
            user_dict[queue["user"]] = {"RUNNING": 1}
        elif queue["state"] == "PENDING":
            user_dict[queue["user"]] = {"PENDING": 1}
        elif queue["state"] == "SUSPENDED":
            user_dict[queue["user"]] = {"SUSPENDED": 1}
        elif queue["state"] == "COMPLETING":
            user_dict[queue["user"]] = {"COMPLETING": 1}
        elif queue["state"] == "COMPLETED":
            user_dict[queue["user"]] = {"COMPLETED": 1}
        else:
            user_dict[queue["user"]] = {"OTHER": 1}
    else:
        if queue["state"] == "RUNNING":
            user_dict[queue["user"]]["RUNNING"] += 1
        elif queue["state"] == "PENDING":
            user_dict[queue["user"]]["PENDING"] += 1
        elif queue["state"] == "SUSPENDED":
            user_dict[queue["user"]]["SUSPENDED"] += 1
        elif queue["state"] == "COMPLETING":
            user_dict[queue["user"]]["COMPLETING"] += 1
        elif queue["state"] == "COMPLETED":
            user_dict[queue["user"]]["COMPLETED"] += 1
        else:
            user_dict[queue["user"]]["OTHER"] += 1

for k, v in user_dict.items():
    values = [f"{k1}={v1}" for k1, v1 in v.items()]
    print(
        f"squeueUser,userId={k} {','.join(values)}")

# # Pending/Running resources
for queue in all_queues:
   partition = '"' + str(queue['partition']) + '"'
   state = '"' + queue['state'] + '"'

   print(
       f"queue_resources,account={queue['account']},partition={queue['partition']},state={queue['state']} nodes={queue['nodes']},cpus={queue['cpus']}")
