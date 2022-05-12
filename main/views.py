from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Category, Cart, Attractions, City


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


def add_attraction(request, id):
    if not request.user.is_authenticated:
        return redirect('/login/')
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


def cart(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    try:
        cart = Cart.objects.get(user=request.user, completed=False)
    except Cart.DoesNotExist:
        return render(request, "main/cart_empty.html", {})
    attractions_list = list(cart.attractions.all())
    if attractions_list:
        return render(request, "main/cart.html", {"attraction_list": attractions_list})
    else:
        return render(request, "main/cart_empty.html", {})


def about(request):
    return render(request, "main/about.html")