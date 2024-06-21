from optimal import get_optimal_route
from distance import calculate_distance_matrix
import pandas as pd

# excel sheet path that contains the customer data
path_1 = r"Book1.xlsx"

# read the given excel sheet
data = pd.read_excel(
    path_1,
    engine='openpyxl',
    )

# assign customer_ID, latitude and longitude values into separate lists
id = map(str, list(data.ACCOUNT_NO))
lat = list(data.LAT)
lon = list(data.LON)
name = list(data.NAME)

# construct the places nested list
places = list(zip(id, lat, lon, name))

# construct the distance matrix
matrix = calculate_distance_matrix(places)

# using google map, construct the optimal route
order, distance = get_optimal_route(matrix)

# generate the direction url for google map direction
directions_url = f"https://www.google.com/maps/dir/?api=1&origin={places[0][2]},{places[0][1]}&destination={places[0][2]},{places[0][1]}&travelmode=driving&waypoints="

# new ordered excel sheet
new_id = []
new_name = []
j = 0
for i in order:
    new_id.append(places[i][0])
    new_name.append(places[i][3])

dF1 = pd.DataFrame(new_name, new_id)
dF1.to_excel('Optimally_Ordered.xlsx', sheet_name='Book2')

print("Your Optimally Ordered excel sheet is prepared")
print(directions_url)
