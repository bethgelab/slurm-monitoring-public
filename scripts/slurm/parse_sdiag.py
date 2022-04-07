#!/bin/env python

import sys
import logging
import re
from datetime import datetime
from time import mktime, time

# sdiag


def strdate_to_ts(s):
    return int(mktime(datetime.strptime(s.strip(), "%a %b %d %H:%M:%S %Y").timetuple()))


root_patterns = {
    # Server thread count: 5
    # Agent queue size:    0
    # Jobs submitted: 2915
    # Jobs started:   1707
    # Jobs completed: 1653
    # Jobs canceled:  20
    # Jobs failed:    0
    # Data since      Sun Jun 21 17:00:00 2015
    'thread_count':     re.compile(r"Server thread count:\s*(?P<thread_count>\d*)"),
    'agent_queue_size': re.compile(r"Agent queue size:\s*(?P<agent_queue_size>\d*)"),
    'jobs.submitted':   re.compile(r"Jobs submitted:\s*(?P<submitted>\d*)"),
    'jobs.started':     re.compile(r"Jobs started:\s*(?P<started>\d*)"),
    'jobs.completed':   re.compile(r"Jobs completed:\s*(?P<completed>\d*)"),
    'jobs.canceled':    re.compile(r"Jobs canceled:\s*(?P<canceled>\d*)"),
    'jobs.failed':      re.compile(r"Jobs failed:\s*(?P<failed>\d*)"),
    'data_since':      (re.compile(r"Data since\s*(?P<data_since>\w+\s+\w+\s+\d+\s+\d+[:]\d+[:]\d+\s+\d+)\s*.*"), strdate_to_ts),
}

sched_main_patterns = {
    # Last cycle:   11079
    # Max cycle:    123872
    # Total cycles: 2724
    # Mean cycle:   17276
    # Mean depth cycle:  314
    # Cycles per minute: 13
    # Last queue length: 2176
    'last_cycle_usec': re.compile(r"\s*Last cycle:\s*(?P<last_cycle_usec>\d*)"),
    'max_cycle_usec': re.compile(r"\s*Max cycle:\s*(?P<max_cycle_usec>\d*)"),
    'total_cycles': re.compile(r"\s*Total cycles:\s*(?P<total_cycles>\d*)"),
    'mean_cycle_usec': re.compile(r"\s*Mean cycle:\s*(?P<mean_cycle_usec>\d*)"),
    'mean_depth_cycle': re.compile(r"\s*Mean depth cycle:\s*(?P<mean_depth_cycle>\d*)"),
    'cycles_per_minute': re.compile(r"\s*Cycles per minute:\s*(?P<cycles_per_minute>\d*)"),
    'last_queue_length': re.compile(r"\s*Last queue length:\s*(?P<last_queue_length>\d*)"),
}

sched_backfill_patterns = {
    # Total backfilled jobs (since last slurm start): 3310
    # Total backfilled jobs (since last stats cycle start): 102
    # Total cycles: 289
    # Last cycle when: Sun Jun 21 19:42:02 2015
    # Last cycle: 2513675311
    # Mean cycle: 7318652
    # Last depth cycle: 2534
    # Last depth cycle (try sched): 60
    # Depth Mean: 3024
    # Depth Mean (try depth): 62
    # Last queue length: 2713
    # Queue length mean
    'total_bf_jobs': re.compile(r"\s*Total backfilled jobs \(since last slurm start\):\s*(?P<total_bf_jobs>\d*)"),
    'total_bf_jobs_since_reset': re.compile(r"\s*Total backfilled jobs \(since last stats cycle start\):\s*(?P<total_bf_jobs_since_reset>\d*)"),
    'total_cycles': re.compile(r"\s*Total cycles:\s*(?P<total_cycles>\d*)"),
    'last_cycle_time': (re.compile(r"Last cycle when:\s*(?P<last_cycle_time>\w+\s+\w+\s+\d+\s+\d+[:]\d+[:]\d+\s+\d+)\s*.*"), strdate_to_ts),
    'last_cycle_usec': re.compile(r"\s*Last cycle:\s*(?P<last_cycle_usec>\d*)"),
    'mean_cycle_usec': re.compile(r"\s*Mean cycle:\s*(?P<mean_cycle_usec>\d*)"),
    'last_depth_cycle': re.compile(r"\s*Last depth cycle:\s*(?P<last_depth_cycle>\d*)"),
    'last_depth_cycle_try': re.compile(r"\s*Last depth cycle \(try sched\):\s*(?P<last_depth_cycle_try>\d*)"),
    'depth_mean': re.compile(r"\s*Depth Mean:\s*(?P<depth_mean>\d*)"),
    'depth_mean_try': re.compile(r"\s*Depth Mean \(try depth\):\s*(?P<depth_mean_try>\d*)"),
    'last_queue_length': re.compile(r"\s*Last queue length:\s*(?P<last_queue_length>\d*)"),
    'queue_length_mean': re.compile(r"\s*Queue length mean:\s*(?P<queue_length_mean>\d*)"),

}


section = 'sdiag'

data = {}

for line in sys.stdin:

    #logging.info(f"> {line}")

    if line.startswith("Main schedule statistics"):
        section = "scheduler_main"
    elif line.startswith("Backfilling stats"):
        section = "scheduler_backfill"

    if section and not section in data:
        data[section] = {}

    if section == "sdiag":
        for key, pat in root_patterns.items():
            if type(pat) is tuple:
                pat, fun = pat
            else:
                def fun(x): return x
            match = pat.match(line)
            if match:
                #print( "%s.%s %s" % (section, key, fun(match.group(key.split('.')[-1]))) )
                data[section][key] = fun(match.group(key.split('.')[-1]))

    elif section == "scheduler_main":
        for key, pat in sched_main_patterns.items():
            match = pat.match(line)
            if match:
                #print( "%s.%s %s" % (section, key, match.group(key) ) )
                data[section][key] = match.group(key)

    elif section == "scheduler_backfill":
        for key, pat in sched_backfill_patterns.items():
            if type(pat) is tuple:
                pat, fun = pat
            else:
                def fun(x): return x
            match = pat.match(line)
            if match:
                #print( "%s.%s %s" % (section, key, fun(match.group(key)) ) )
                data[section][key] = fun(match.group(key))


for section in data.keys():
    values = [f"{k}={data[section][k]}" for k in data[section].keys()]
    print(f"sdiag,section={section} {','.join(values)}")
