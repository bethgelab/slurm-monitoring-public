#!/bin/bash
# Start collection of the metrics
source .env && nohup telegraf --config telegraf/telegraf.conf &