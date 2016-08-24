import requests
import json
import psycopg2  #for postgres connection
import psycopg2.extras
import yahooID    #for convert fantasyID to yahooID
import statsToUpdate
import datetime
import time

try:
  # conn = psycopg2.connect("dbname='d41t17krm7a40' user='blagfvvvucxgkt' host='ec2-50-17-255-49.compute-1.amazonaws.com' password='lsqSj-7P24N-W9sT2DRHcxG260'")
  conn = psycopg2.connect("dbname='nflsportify' user='nflguru' host='nflsportify.c3mi87ty0bem.us-west-2.rds.amazonaws.com' password='nflgurusports2'")
  print ("Connected to db")
  cur = conn.cursor()
  
  # url = 'https://api.fantasydata.net/v3/nfl/projections/JSON/PlayerGameProjectionStatsByWeek/2016REG/1'
  url = 'https://api.fantasydata.net/v3/nfl/projections/JSON/PlayerSeasonProjectionStats/2016REG'
  headers = { 'Ocp-Apim-Subscription-Key' : '2c941f2a2989457fa95fbc54ab8de154' }

  r = requests.get(url, headers = headers)
  parsed_json = json.loads(r.text)
  counter = 0

  plen = len(parsed_json)

  while (counter < plen) :
    row = parsed_json[counter]
    print('row------------')

    fanID = row.get('PlayerID')
    yID = yahooID.lookup.get(fanID, None) #[fanID]
    print('yID')
    if (yID == None) :
      print('yID NOT FOUND')
    else :
      print(yID)

      values = []
      for item in statsToUpdate.stats :
        thisval = row.get(item, 0)
        if (isinstance(thisval, float)):
          thisval = int(round(thisval))
        values.append('\"{0}\" = \'{1}\''.format(item, thisval))

      valueString = ', '.join(str(elem) for elem in values)
      updateStatement = 'UPDATE \"playerProjectedYears\" SET {0} WHERE "Season" = 2016 AND "playerId" = {1};'.format(valueString, yID)
      print('updateStatement')
      print(updateStatement)
      try:
        print('lastIndex')
        print(counter)
        cur.execute(updateStatement)
        conn.commit()
      except ValueError as err:
        print ("Cannot INSERT to database {0}".format(err))
    print(counter)
    counter += 1
  print('Hello World, ALL DONE');

except OSError as err:
  print ("OS error: {0}".format(err))
except ValueError as err:
  print ("Cannot connect to database {0}".format(err))

conn.close()