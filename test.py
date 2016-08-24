import json

print('cron job running')

allPlayers = ['hello']

with open('/Users/ducpham/hackreactor/thesis/pythonTools/test.txt', 'w') as outfile:
  json.dump(allPlayers, outfile)