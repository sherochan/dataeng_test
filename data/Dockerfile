FROM python:3.6

#install python
COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get update && apt-get -y install cron

RUN apt-get update && apt-get -y install vim

# Add crontab file in the cron directory
# ADD cronjob /etc/cron.d/container_cronjob

ADD data_processing_Q1.py /data_processing_Q1.py
ADD run_data_processing.sh /run_data_processing.sh
ADD entrypoint.sh /entrypoint.sh

RUN chmod +x /run_data_processing.sh /entrypoint.sh


# Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# Run the command on container startup
ENTRYPOINT /entrypoint.sh
# CMD cron -f && tail -f /var/log/cron.log
# CMD [/bin/sh, “-c”, “/run_data_processing.sh && chmod 644 /etc/cron.d/container_cronjob && cron && tail -f /var/log/cron.log”]