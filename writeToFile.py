import psycopg2
import psycopg2.extras
# import psycopg2.extras
import json
import statsToUpdate


def addQuotes(string):
  return '\"' + string + '\"'

mappedStats = map(addQuotes, statsToUpdate.stats)

selectFields = ", ".join(mappedStats)
print(selectFields)

allPlayers = {}

try:
  conn = psycopg2.connect("dbname='d41t17krm7a40' user='blagfvvvucxgkt' host='ec2-50-17-255-49.compute-1.amazonaws.com' password='lsqSj-7P24N-W9sT2DRHcxG260'")
  print ("Connected to db")
  # cur = conn.cursor()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

  selectStatement = 'SELECT {0} FROM \"playerProjectedGames\" WHERE \"playerId\" = {1};'.format(selectFields, 7200)
  print('selectStatement')
  print(selectStatement)

  cur.execute(selectStatement)
  records = cur.fetchone()

  recdict = {}
  for key in statsToUpdate.stats:
    recdict[key] = records[key]

  print('dict')
  print(recdict)

  allPlayers['7200'] = recdict

  with open('update-projections.txt', 'w') as outfile:
    json.dump(allPlayers, outfile)

except ValueError as err:
  print ("Cannot connect to database {0}".format(err))

