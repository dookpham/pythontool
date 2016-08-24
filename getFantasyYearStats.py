import requests
import json
import psycopg2  #for postgres connection
import psycopg2.extras
import yahooID    #for convert fantasyID to yahooID
import statsDict    #for convert fantasyID to yahooID
import datetime
import time

# tempID = yahooID.lookup[2428]
# print('tempID')
# print(tempID)

# sFiller = []
fields = []
for key in statsDict.kvpairs :
  fields.append(key)
  # sFiller.append('%s')
fieldString = ', '.join('"' + elem + '"' for elem in fields)
fieldString = fieldString + ', "createdAt", "updatedAt", "playerId"'
print(fieldString)

# psql --host=ec2-50-17-255-49.compute-1.amazonaws.com --port=5432 --username=blagfvvvucxgkt  --dbname=d41t17krm7a40

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
      for key in fields :
        value = row.get(key, 0)
        if (value == None) :
          value = '0' #'\'null\''
        elif (isinstance(value, str)):
          value = value.replace('\'', ' ')
          value = '\'' + value + '\''
        values.append(value)

      values.append('now()')
      values.append('now()')
      values.append(yID)
      valueString = ', '.join(str(elem) for elem in values)
      insertStatement = 'INSERT INTO \"playerProjectedYears\" ({0}) VALUES ({1}) WHERE "Season" = 2016;'.format(fieldString, valueString)
      print('insertStatement')
      print(insertStatement)
      try:
        print('lastIndex')
        print(counter)
        cur.execute(insertStatement)
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