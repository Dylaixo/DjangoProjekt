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
    for i in range(0, y):
        for j in range(i, y):
            route = get_route(attractions_list[j].long, attractions_list[j].lat,
                                       attractions_list[i].long, attractions_list[i].lat)
            routes[j][i] = routes[i][j] = route['duration']
    distance = 0
    permutation = [0]
    routes_visited = np.zeros(y)
    routes_visited[0] = 1
    start = 0
    for i in range(0, y-1):
        min_dist = (99999999, 0)
        for j in range(i+1, y):
            if routes_visited[j] == 0 and min_dist[0] > routes[start][j]:
                min_dist = (routes[start][j], j)
        permutation.append(min_dist[1])
        distance += min_dist[0]
        routes_visited[min_dist[1]] = 1
        start = min_dist[1]
    return permutation, distance


