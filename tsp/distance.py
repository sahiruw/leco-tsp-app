import requests


def get_distance(start, end):
    url = f"https://routing.openstreetmap.de/routed-car/route/v1/driving/{start[0]},{start[1]};{end[0]},{end[1]}?overview=false&alternatives=true&steps=true"

    response = requests.get(url).json()
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