import json
import sqlite3
import urllib.request
import re

max_alt = 2700  #Max alt to look for plane

#this funtion find the closest plane that our antenna receives
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
        #print("Data from nearest flight (from function nearest plane): " , nearest_flight)
        return "%s" % (nearest_flight["flight"].strip())
    except IndexError:
        return

#====================================================

#This function gives us the route from flight number using the PAI from https://api.joshdouch.me
def get_route_API(flight_number):
    try:
        with urllib.request.urlopen("https://api.joshdouch.me/callsign-route.php?callsign="+flight_number) as url:
            route = url.read().decode()
            print(route)
            return route.split("-")
    except:
        return
#this one alos gives us the route from the flight number, using data from virtualradarserver.co.uk
def get_route_SQL(flight_number):
    try:
        # regex to split airline code from flight number
        flight_number_re = re.compile( "^([A-Z]{3})?(\d[A-Z0-9]*)$")
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
print("Flight number : ", get_the_nearest_airplane())
print("=====1")
print("=====2")
print("Its route using API is : ",get_route_API(get_the_nearest_airplane()))
print("Its route using SQL is: ",get_route_SQL(get_the_nearest_airplane()))
#print("=====2")
#print("la route du vol SVA022 est (API) : ",get_route_API("SVA022"))
#print("la route du vol SVA022 est (SQL) : ",get_route_SQL("SVA022"))
#print("=====2")
