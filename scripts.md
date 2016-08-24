
# dump from main db into a .sql file
pg_dump --host=nflsportify.c3mi87ty0bem.us-west-2.rds.amazonaws.com --port=5432 --username=nflguru --dbname=nflsportify -t '"playerProjectedGames"' > playerProjectedGames.sql

# dump from .sql file into db
psql --host=ec2-50-17-255-49.compute-1.amazonaws.com --port=5432 --username=blagfvvvucxgkt  --dbname=d41t17krm7a40 -a -f playerProjectedGames.sql

