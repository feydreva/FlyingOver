import json
import sqlite3
import urllib.request
import re



max_alt = 70000  #altitude max de recherche d'avion


#cette function cherche l'avion le plus pret de soit, parmis les avion captés
def get_the_nearest_airplane():
    with urllib.request.urlopen("http://10.0.0.95/dump1090-fa/data/aircraft.json") as url:
        aircraft_json = json.loads(url.read().decode())
    with urllib.request.urlopen("http://10.0.0.95/dump1090-fa/data/receiver.json") as url:
        location_json = json.loads(url.read().decode())

    aircraft_list = aircraft_json.get("aircraft")
    aircraft_list = [f for f in aircraft_list if "flight" in f and f["seen"] < 15 and f["alt_baro"] < max_alt]


    def distance(f):
          return ((f.get("lat", 0) - location_json["lat"]) ** 2 + (f.get("lon", 0) - location_json["lon"]) ** 2) ** 0.5

    try:
        nearest_flight = sorted(aircraft_list, key=distance)[0]
        print("Info du vol le plus proche (de la fucntion nearest plane): " , nearest_flight)
        return "%s" % (nearest_flight["flight"].strip())
    except IndexError:
        return


#====================================================
#Si on utilise les donnée / API du site joshdouch.me
#cette function nous donne la routre a partir d'un call sign de vol
def get_route(flight_number):
    try:
        # Si on utilise les donnée / API du site joshdouch.me
        # cette function nous donne la routre a partir d'un call sign de vol
        with urllib.request.urlopen("https://api.joshdouch.me/callsign-route.php?callsign="+flight_number) as url:
            route = url.read().decode()
            print(route)
            return route.split("-")
    except:
        try:
            a
            # Si on utilise les données du site virtualradarserver.co.uk
            # regex pour séparer la companie "airline code" et le niumero de vol "flight number"
            flight_number_re = re.compile( "^([A-Z]+)?(\d+)$" )
            airline, number = flight_number_re.match( flight_number ).groups()
            con = sqlite3.connect( 'flightnumbers.sqlite3' )
            cur = con.cursor()
            flight_infos = list(cur.execute( '''SELECT * FROM flightnumbers where AirlineCode = ? and FlightNumber = ?''', (airline, number) ) )
            con.close()
            flight_infos = flight_infos[0]
            flight_infos = flight_infos[2:]
            flight_infos = list( flight_infos )
            for c in flight_infos:
                split_lines = c.split( "-" )
            return [split_lines[0], split_lines[1]]
        except:
            return




print("=====1")
print("Numero de Vol : ", get_the_nearest_airplane())
print("=====1")
print("=====2")
print("Sa route est : ",get_route(get_the_nearest_airplane()))
print("=====2")

print("la route du vol SVA022 est : ",get_route("SVA022"))
print("=====2")
print("=====3")
flight_number = "SVA1022"
print(flight_number)

# Si on utilise les données du site virtualradarserver.co.uk
# regex pour séparer la companie "airline code" et le niumero de vol "flight number"

flight_number_re = re.compile( "^([A-Z]+)?(\d+)$")
airline, number = flight_number_re.match( flight_number ).groups()
con = sqlite3.connect('flightnumbers.sqlite3')
cur = con.cursor()
flight_infos = list(cur.execute('''SELECT * FROM flightnumbers where AirlineCode = ? and FlightNumber = ?''', (airline, number)))
con.close()
flight_infos = flight_infos[0]
flight_infos=flight_infos[2:]
flight_infos=list(flight_infos)
for c in flight_infos:
    split_lines = c.split("-")
route = [split_lines[0],split_lines[1]]

print(route)