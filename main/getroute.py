import requests
import polyline
import folium
import json


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


def shortest_path(attracions_list):
    locations_tmp = []
    for index, attracion in enumerate(attracions_list):
        tmp = f'"address":"{index + 1}","lat":"{attracion.lat}","lng":"{attracion.long}"'
        locations_tmp.append("{"+tmp+"}")
    locations = {"locations": "[" + ','.join(locations_tmp) + "]"}
    url = 'https://api.routexl.com/tour'
    username = 'C2g'
    password = 'pilkoryj1'
    g = requests.post(url, auth=(username, password), data=locations)
    data = json.loads(g.text)
    permutation = []
    tmp_distance = []
    distance = []
    for key in data['route']:
        permutation.append(int(data['route'][key]['name']) - 1)
    for i in range(1, len(permutation)):
        dist = get_route(attracions_list[permutation[i]].long, attracions_list[permutation[i]].lat,
                         attracions_list[permutation[i-1]].long, attracions_list[permutation[i-1]].lat)
        distance.append(round(dist['duration']/60))
    return permutation, distance


def generate_map(attractions_list, distance):
    figure = folium.Figure()
    m = folium.Map(location=[attractions_list[0].lat,
                             attractions_list[0].long],
                   zoom_start=15)
    m.add_to(figure)
    for i in range(1, len(attractions_list)):
        route = get_route(attractions_list[i - 1].long, attractions_list[i - 1].lat, attractions_list[i].long,
                          attractions_list[i].lat)
        folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6,tooltip=f"{distance[i-1]} min.").add_to(m)
        frame = folium.IFrame(attractions_list[i - 1].name, width=100, height=30)
        folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='green'),
                      popup=folium.Popup(frame, max_width=100)).add_to(m)
        frame = folium.IFrame(attractions_list[i].name, width=100, height=30)
        folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red'),
                      popup=folium.Popup(frame, max_width=100)).add_to(m)
        figure.render()
    return figure
