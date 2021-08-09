import json
import sqlite3
import urllib.request
import re

#flight_number = "SVA1022"
#flight_number = "TVS3407"
flight_number = "AAF261C"

# Si on utilise les données du site virtualradarserver.co.uk
# regex pour séparer la companie "airline code" et le niumero de vol "flight number"
flight_number_re = re.compile( "^([A-Z]+)?(\d+)$")
flight_number_re = re.compile("^([A-Z]{3})?(\d[A-Z0-9]*)$")
airline, number = flight_number_re.match( flight_number ).groups()
print(airline, number)
con = sqlite3.connect( 'flightnumbers.sqlite3' )
cur = con.cursor()
flight_infos = list(
    cur.execute( '''SELECT * FROM flightnumbers where AirlineCode = ? and FlightNumber = ?''', (airline, number) ) )
con.close()
flight_infos = flight_infos[0]
flight_infos = flight_infos[2:]
flight_infos = list( flight_infos )
for c in flight_infos:
    split_lines = c.split( "-" )
print([split_lines[0], split_lines[1]])