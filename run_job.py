from crontab import CronTab
import os

cwd = os.getcwd()
cron = CronTab(user='sahel')
job = cron.new(command='python3 ' + cwd + '/getDiscount.py')
job.minute.every(3)

cron.write()
