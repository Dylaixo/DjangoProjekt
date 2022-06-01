from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Category, Cart, Attractions, City
from django.contrib.auth.decorators import login_required
from . import getroute
import folium
from django.http import HttpResponseNotFound
from django.db.models import Sum


def generate_default_carts(city=None):
    try:
        default = User.objects.get(username="default")
        default_list = Cart.objects.filter(user=default)
        if city is not None:
            default_list_filtered = list()
            for cart in default_list:
                if list(cart.attractions.all())[0].city.name == city:
                    default_list_filtered.append(cart)
            return default_list_filtered
    except Exception as e:
        default_list = ()
    return default_list

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
    context = {"attraction_list": attraction_list, "city": city,
               "default_list": generate_default_carts(city)}
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
        cart = Cart(user=user, completed=False, first_attraction=attraction[0])
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
        return render(request, "main/cart_empty.html", {"default_list": generate_default_carts()})
    if request.GET.get('del_attraction'):
        tmp_attraction = Attractions.objects.get(id=request.GET.get('attraction_id'))
        cart.attractions.remove(tmp_attraction)
    attractions_list = list(cart.attractions.all())
    if attractions_list:
        first_attraction = cart.first_attraction
        if request.GET.get('change_first'):
            first_attraction = Attractions.objects.get(id=request.GET.get('attraction_id'))
        for index, attraction in enumerate(attractions_list):
            if attraction == first_attraction:
                attractions_list.remove(attraction)
                attractions_list.insert(0, attraction)
        permutation, distance = getroute.shortest_path(attractions_list)
        tmp_list = []
        for i in permutation:
            tmp_list.append(attractions_list[i])
        figure = getroute.generate_map(tmp_list)
        price = cart.attractions.all().aggregate(Sum('price'))['price__sum']
        time = int(distance / 60) + cart.attractions.all().aggregate(Sum('time'))['time__sum']
        return render(request, "main/cart.html", {"attraction_list": tmp_list, "map": figure, "time": time,
                                                  "del": True, "price": price})
    else:
        return render(request, "main/cart_empty.html", {"default_list": generate_default_carts()})


def cart_show(request, id):
    cart = Cart.objects.get(id=id)
    if request.user != cart.user and cart.user.username != "default":
        return HttpResponseNotFound("You dont have permissions")
    attractions_list = list(cart.attractions.all())
    first_attraction = cart.first_attraction
    for index, attraction in enumerate(attractions_list):
        if attraction == first_attraction:
            attractions_list.remove(attraction)
            attractions_list.insert(0, attraction)
    duration = 0
    figure = getroute.generate_map(attractions_list)
    price = cart.attractions.all().aggregate(Sum('price'))['price__sum']
    time = int(duration / 60) + cart.attractions.all().aggregate(Sum('time'))['time__sum']
    return render(request, "main/cart.html",
                  {"attraction_list": attractions_list, "map": figure, "time": time,
                   "del": False, "price": price})


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
