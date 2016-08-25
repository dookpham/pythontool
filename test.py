import time
import json

def job():
  print('cron job running')
  allPlayers = ['hello']
  with open('/usr/src/app/test.txt', 'w') as outfile:
    json.dump(allPlayers, outfile)
  time.sleep(60)
  job()

job()


