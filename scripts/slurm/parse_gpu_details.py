import sys
import datetime

format_dict = {}
for line in sys.stdin:
    out_vals = line.split(",")
    cleaned_vals = []
    # Clean
    for val in out_vals:
        val = val.replace(" ", "")
        val = val.replace("\n", "")
        if "N/A" in val:
            val = 0
        elif ":" in val:
            val = val.split(":")[-1]
        cleaned_vals.append(val)

    if cleaned_vals[0] not in format_dict:
        format_dict[cleaned_vals[0]] = {
            "t_cpu": int(cleaned_vals[1]), "t_gpu": int(cleaned_vals[2])}
    else:
        format_dict[cleaned_vals[0]]["t_cpu"] += int(cleaned_vals[1])
        format_dict[cleaned_vals[0]]["t_gpu"] += int(cleaned_vals[2])

for k, v in format_dict.items():
    values = [f"{k1}={v1}" for k1, v1 in v.items()]
    print(f"usage_details,partition={k} {','.join(values)}")
