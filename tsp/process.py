
from optimal import get_optimal_route
from distance import calculate_distance_matrix,get_station_coordinates
import pandas as pd



def process_file(data, stationName):
    # assign customer_ID, latitude and longitude values into separate lists
    id = map(str, list(data.ACCOUNT_NO))
    lat = list(data.LAT)
    lon = list(data.LON)
    name = list(data.NAME)

    # construct the places nested list
    places = list(zip(id, lat, lon, name))

    stationCordinates = get_station_coordinates(stationName)
    stationCordinates.insert(0, "station")
    stationCordinates.append(stationName)

    places.insert(0, stationCordinates)

    print(places)
    # construct the distance matrix
    matrix = calculate_distance_matrix(places)


    # using google map, construct the optimal route
    order, distance = get_optimal_route(matrix)

    # generate the direction url for google map direction
    directions_url = f"https://www.google.com/maps/dir/?api=1&origin={places[0][2]},{places[0][1]}&destination={places[0][2]},{places[0][1]}&travelmode=driving&waypoints="

    # new ordered excel sheet
    data = []

    for j, i in enumerate(order):
        print(places[i][0], end=" -> ")
        if i != 0 and i != len(order) - 1:
            directions_url += f"{places[i][2]},{places[i][1]}|"
        data.append({
            "ACCOUNT_NO": places[i][0],
            "LAT": places[i][1],
            "LON": places[i][2],
            "NAME": places[i][3],
            "ORDER": j
        })

    print(directions_url)
    return data, distance, directions_url