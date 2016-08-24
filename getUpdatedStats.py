import requests
import json
import psycopg2  #for postgres connection
import psycopg2.extras
import yahooID    #for convert fantasyID to yahooID
import statsDict    #for convert fantasyID to yahooID
import statsToUpdate
import datetime
import time
import numbers

def addQuotes(string):
  return '\"' + string + '\"'

mappedStats = map(addQuotes, statsToUpdate.stats)

selectFields = ", ".join(mappedStats)
print(selectFields)

allPlayers = []

fields = []
for key in statsDict.kvpairs :
  fields.append(key)
fieldString = ', '.join('"' + elem + '"' for elem in fields)
fieldString = fieldString + ', "createdAt", "updatedAt", "playerId"'
print(fieldString)


try:
  conn = psycopg2.connect("dbname='d41t17krm7a40' user='blagfvvvucxgkt' host='ec2-50-17-255-49.compute-1.amazonaws.com' password='lsqSj-7P24N-W9sT2DRHcxG260'")
  print ("Connected to db")
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

  url = 'https://api.fantasydata.net/v3/nfl/projections/JSON/PlayerGameProjectionStatsByWeek/2016REG/1'
  headers = { 'Ocp-Apim-Subscription-Key' : '2c941f2a2989457fa95fbc54ab8de154' }

  r = requests.get(url, headers = headers)
  parsed_json = json.loads(r.text)
  counter = 0

  plen = len(parsed_json)
  # plen = 5 # for testing

  while (counter < plen) :
    row = parsed_json[counter]
    fanID = row.get('PlayerID')
    yID = yahooID.lookup.get(fanID, None) #[fanID]
    if (yID == None) :
      print('yID NOT FOUND')
    else :
      print(yID)

      # get the current projected stats
      selectStatement = 'SELECT {0} FROM \"playerProjectedGames\" WHERE \"playerId\" = {1} AND \"Season\" = 2016 AND \"Week\" = 1 LIMIT 1;'.format(selectFields, yID)
      print('selectStatement')
      print(selectStatement)

      cur.execute(selectStatement)
      records = cur.fetchone()

      needsUpdate = False
      if (records):
        for key in statsToUpdate.stats:
          # print(key)
          # print(row[key])
          # print(row[key])
          getRow = row.get(key, None)
          getRecord = records.get(key, None)

          if (getRow != None and getRecord != None):
            value = round(getRow)
            if (isinstance(getRecord, int) and isinstance(value, int) and getRecord != value):
              print('-------------------------------------------------')
              print(key)
              print(getRecord)
              print(value)
              print('-------------------------------------------------')
              needsUpdate = True

      if (needsUpdate == True):
        allPlayers.append(yID)

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
        insertStatement = 'INSERT INTO \"playerProjectedGames\" ({0}) VALUES ({1});'.format(fieldString, valueString)
        print('insertStatement')
        print(insertStatement)
        try:
          print('lastIndex')
          print(counter)
          cur.execute(insertStatement)
          conn.commit()
        except ValueError as err:
          print ("Cannot INSERT to database {0}".format(err))
      else :
        print('Player doesnt need to update: {0}'.format(yID))

    print(counter)
    counter += 1
  print('Hello World, ALL DONE');

except OSError as err:
  print ("OS error: {0}".format(err))
except ValueError as err:
  print ("Cannot connect to database {0}".format(err))

print('allPlayers')
print(allPlayers)

if (len(allPlayers) > 0):
  with open('update-players.txt', 'w') as outfile:
    json.dump(allPlayers, outfile)


conn.close()