from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Category, Cart, Attractions, City
from django.contrib.auth.decorators import login_required
from . import getroute
import folium
from django.http import HttpResponseNotFound
from django.db.models import Sum


def index(request):
    return render(request, "main/index.html", {})


def home(request):
    return render(request, "main/home.html")


def cities(request):
    city_list = City.objects.all()
    context = {"city_list": city_list}
    return render(request, "main/cities.html", context)


def attractions(request, city):
    attraction_list = Attractions.objects.all()
    context = {"attraction_list": attraction_list, "city": city}
    return render(request, "main/attractions.html", context)


def single_attraction(request, id):
    attraction = Attractions.objects.get(id=id)
    context = {"attraction": attraction}
    return render(request, "main/single_attraction.html", context)


@login_required()
def add_attraction(request, id):
    user = User.objects.get(id=request.user.id)
    queryset = Cart.objects.filter(user=user, completed=False)
    attraction = Attractions.objects.filter(id=id)
    try:
        cart = Cart.objects.get(user=user, completed=False)
    except Cart.DoesNotExist:
        cart = Cart(user=user, completed=False)
        cart.save()
    cart.attractions.add(attraction[0])
    return redirect(f"/attractions/single_attraction/{id}")


@login_required()
def cart(request):
    if request.GET.get('clicked'):
        cart = Cart.objects.get(user=request.user, completed=False)
        cart.completed = True
        cart.save()
    try:
        cart = Cart.objects.get(user=request.user, completed=False)
    except Cart.DoesNotExist:
        return render(request, "main/cart_empty.html", {})
    attractions_list = list(cart.attractions.all())
    if attractions_list:
        figure = folium.Figure()
        m = folium.Map(location=[attractions_list[0].lat,
                                 attractions_list[0].long],
                       zoom_start=10)
        m.add_to(figure)
        permutation, distance = getroute.shortest_path(attractions_list)
        tmp_list = []
        for i in permutation:
            tmp_list.append(attractions_list[i])
        for i in range(1, len(tmp_list)):
            route = getroute.get_route(attractions_list[i-1].long, attractions_list[i-1].lat, attractions_list[i].long,
                                       attractions_list[i].lat)
            folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
            folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
            folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
            figure.render()
        price = cart.attractions.all().aggregate(Sum('price'))['price__sum']
        time = int(distance/60) + cart.attractions.all().aggregate(Sum('time'))['time__sum']
        return render(request, "main/cart.html", {"attraction_list": attractions_list, "map": figure, "time": time, "del": True, "price": price})
    else:
        return render(request, "main/cart_empty.html", {})


def cart_show(request, id):
    cart = Cart.objects.get(id=id)
    if request.user is not cart.user:
        return HttpResponseNotFound("Cant find that cart")
    attractions_list = list(cart.attractions.all())
    figure = folium.Figure()
    m = folium.Map(location=[attractions_list[0].lat,
                             attractions_list[0].long],
                   zoom_start=10)
    m.add_to(figure)
    duration = 0
    for i in range(1, len(attractions_list)):
        route = getroute.get_route(attractions_list[i - 1].long, attractions_list[i - 1].lat, attractions_list[i].long,
                                   attractions_list[i].lat)
        folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
        folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
        folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
        figure.render()
        duration = duration + route['duration']
    return render(request, "main/cart.html",
                  {"attraction_list": attractions_list, "map": figure, "duration": duration, "del": False})


def about(request):
    return render(request, "main/about.html")


@login_required
def profile(request):
    try:
        cart = Cart.objects.get(user=request.user, completed=False)
        attractions_list = list(cart.attractions.all())
    except Cart.DoesNotExist:
        attractions_list = {}
    try:
        cart_list = Cart.objects.filter(user=request.user, completed=True)
    except Cart.DoesNotExist:
        attractions_list = {}
    return render(request, "main/profile.html", {"attraction_list": attractions_list, "cart_list": cart_list})
