from crontab import CronTab
import getpass
 # /home/piyush/Desktop/etfnew/ETFAnalysis/ProcessCaller.py
 # /home/ubuntu/ETFAnalysis/ProcessCaller.py
username = getpass.getuser()
my_cron = CronTab(user=username)
job = my_cron.new(command='python /home/' + username + '/ETFAnalysis/ProcessCaller.py', comment = 'HoldingsCron')
job.hour.on(9)

my_cron.write()