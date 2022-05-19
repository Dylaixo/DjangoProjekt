import requests
import polyline
from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np


def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc)
    if r.status_code != 200:
        return {}
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    duration = res['routes'][0]['duration']

    out = {'route': routes,
           'start_point': start_point,
           'end_point': end_point,
           'distance': distance,
           'duration': duration
           }

    return out


def shortest_path(attractions_list):
    y = len(attractions_list)
    routes = np.zeros((y, y))
    for i in range(0, len(attractions_list)):
        for j in range(i, len(attractions_list)):
            route = get_route(attractions_list[j].long, attractions_list[j].lat,
                                       attractions_list[i].long, attractions_list[i].lat)
            routes[j][i] = routes[i][j] = route['duration']
    permutation, distance = solve_tsp_dynamic_programming(routes)
    print(permutation)
    print(distance)
    return permutation, distance


