# Set the base image to Node
FROM python:3.5.2
#FROM ubuntu:latest

# File Author / Maintainer
MAINTAINER DJRC

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

CMD [ "python", "updateFantasyYearStats.py" ]






# add crontab file in the cron director
# ADD crontab /usr/src/app/crontab

# give execution rights on the cron job
# RUN chmod 0644 /usr/src/app/crontab

# create log file to run tail
# RUN touch /usr/src/app/cron.log



# CMD crontab && tail -f /usr/src/app/cron.log
