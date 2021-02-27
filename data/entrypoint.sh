#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

# Setup a cron schedule
# reference from https://blog.knoldus.com/running-a-cron-job-in-docker-container/ 
echo "* 1 * * *  /bin/sh /run_data_processing.sh > ~/cron.log
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f