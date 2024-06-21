import requests


def get_distance(start, end):

    url = f"https://routing.openstreetmap.de/routed-car/route/v1/driving/{start[0]},{start[1]};{end[0]},{end[1]}?overview=false&alternatives=true&steps=true"

    response = requests.get(url).json()
    # print(response)
    route = response['routes'][0]
    distance = route['distance']
    duration = route['duration']

    return distance, duration


def calculate_distance_matrix(palces):
    matrix = []
    for i in range(len(palces)):
        row = []
        for j in range(len(palces)):
            if i == j:
                row.append(0)
            else:
                distance, _ = get_distance(palces[i][1:], palces[j][1:])
                row.append(distance)
        matrix.append(row)
        print(i)
    return matrix


def get_station_coordinates(name):
    return stations[name]


def get_all_station_names():
    return list(stations.keys())


stations = {
    "Galle Depot": [80.20603039982913, 6.049809895178689],
    "Hikkaduwa Depot": [80.10208343141348, 6.140125528516681],
    "Ambalanoda Depot": [80.05679194234325, 6.231228614072956]
}