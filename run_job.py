from crontab import CronTab
import os


cwd = os.getcwd()
cron = CronTab(user='sahel')
command = cwd + '/env/bin/python3 ' + cwd + '/getDiscount.py'

job = cron.new(command=command)

job.minute.every(3)
cron.write()

# for item in cron:
#     cron.remove(item)
#     cron.write()

print(cron)
