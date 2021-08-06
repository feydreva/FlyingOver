import json
import sqlite3
import urllib.request
import re

max_alt = 50000  #altitude max de recherche d'avion


#cette function cherche l'avion le plus pret de soit, parmis les avion captés
def get_the_nearest_airplane():
    with urllib.request.urlopen("http://10.0.0.95/dump1090-fa/data/aircraft.json") as url:
        aircraft_json = json.loads(url.read().decode())
    with urllib.request.urlopen("http://10.0.0.95/dump1090-fa/data/receiver.json") as url:
        location_json = json.loads(url.read().decode())

    aircraft_list = aircraft_json.get("aircraft")
    aircraft_list = [f for f in aircraft_list if "flight" in f and f["seen"] < 15 and f["alt_baro"] < max_alt]

   # print(aircraft_list)

    def distance(f):
          return ((f.get("lat", 0) - location_json["lat"]) ** 2 + (f.get("lon", 0) - location_json["lon"]) ** 2) ** 0.5

    try:
        nearest_flight = sorted(aircraft_list, key=distance)[0]
        return "%s" % (nearest_flight["flight"].strip())
    except IndexError:
        return


#regex pour séparer la companie "airline code" et le niumero de vol "flight number"
flight_number_re = re.compile("^([A-Z]+)?(\d+)$")

#on obtient airline et numero de vol
airline, number = flight_number_re.match(get_the_nearest_airplane()).groups()

#on se connect a la db "flightnumbers.sqlite3" générée par le script "ensure_flightnumbers_vsc_exist.sh"
con = sqlite3.connect('flightnumbers.sqlite3')
cur = con.cursor()
flight_infos = list(cur.execute('''SELECT * FROM flightnumbers where AirlineCode = ? and FlightNumber = ?''', (airline, number)))

con.close()

print(flight_infos)

