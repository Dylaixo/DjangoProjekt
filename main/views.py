from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Cart, Attractions, City
from django.contrib.auth.decorators import login_required
from . import getroute
from django.http import FileResponse,  Http404
from django.db.models import Sum
from .pdf import pdfbuffer
from django.core.exceptions import PermissionDenied


def first_last_when_clicked(request, last_attraction, first_attraction, attractions_list):
    tmp_attraction = Attractions.objects.get(id=request.GET.get('attraction_id'))
    if last_attraction == first_attraction:
        for attraction in attractions_list:
            if attraction != last_attraction:
                tmp_attraction = attraction
                break
    return tmp_attraction


def set_list_first_and_last_attractions(attractions_list, first, last):
    for attraction in attractions_list:
        if attraction == first:
            attractions_list.remove(attraction)
            attractions_list.insert(0, attraction)
        if attraction == last:
            attractions_list.remove(attraction)
            attractions_list.insert(len(attractions_list), attraction)
    return attractions_list



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
    try:
        attraction = Attractions.objects.get(id=id)
    except Attractions.DoesNotExist:
        raise Http404
    context = {"attraction": attraction}
    return render(request, "main/single_attraction.html", context)


@login_required()
def add_attraction(request, id):
    user = User.objects.get(id=request.user.id)
    queryset = Cart.objects.filter(user=user, completed=False)
    try:
        attraction = Attractions.objects.filter(id=id)
    except Attractions.DoesNotExist:
        raise Http404
    try:
        cart = Cart.objects.get(user=user, completed=False)
    except Cart.DoesNotExist:
        cart = Cart(user=user, completed=False, first_attraction=attraction[0])
        cart.save()
    cart.attractions.add(attraction[0])
    return redirect(f"/attractions/single_attraction/{id}")


@login_required()
def cart(request):

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
        last_attraction = cart.last_attraction
        if first_attraction is None or last_attraction is None:
            first_attraction = attractions_list[0]
            if len(attractions_list) == 1:
                last_attraction = attractions_list[0]
            else:
                last_attraction = attractions_list[1]
        if request.GET.get('change_first'):
            first_attraction = first_last_when_clicked(request, last_attraction, first_attraction, attractions_list)
        if request.GET.get('change_last'):
            last_attraction = first_last_when_clicked(request, last_attraction, first_attraction, attractions_list)
        cart.first_attraction = first_attraction
        cart.last_attraction = last_attraction
        cart.save()
        attractions_list = set_list_first_and_last_attractions(attractions_list, first_attraction, last_attraction)
        permutation, distance = getroute.shortest_path(attractions_list)
        if request.GET.get('clicked'):
            cart.distance = ';'.join(str(x) for x in distance)
            cart.completed = True
            cart.save()
        tmp_list = []
        for i in permutation:
            tmp_list.append(attractions_list[i])
        figure = getroute.generate_map(tmp_list, distance)
        price = cart.attractions.all().aggregate(Sum('price'))['price__sum']
        time = int(sum(distance)) + cart.attractions.all().aggregate(Sum('time'))['time__sum']
        return render(request, "main/cart.html", {"attraction_list": tmp_list, "map": figure, "time": time,
                                                  "del": True, "price": price})
    else:
        return render(request, "main/cart_empty.html", {"default_list": generate_default_carts()})


def cart_show(request, id):
    try:
        cart = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        raise Http404

    if request.user != cart.user and cart.user.username != "default":
        raise PermissionDenied()
    attractions_list = list(cart.attractions.all())
    first_attraction = cart.first_attraction
    last_attraction = cart.last_attraction
    attractions_list = set_list_first_and_last_attractions(attractions_list, first_attraction, last_attraction)
    if request.GET.get('pdf'):
        buffer = pdfbuffer(attractions_list)
        return FileResponse(buffer, as_attachment=False, filename='hello.pdf')
    price = cart.attractions.all().aggregate(Sum('price'))['price__sum']
    distance = [int(i) for i in cart.distance.split(';')]
    figure = getroute.generate_map(attractions_list, distance)
    time = sum(distance) + sum(attraction.time for attraction in attractions_list)
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


def custom_page_not_found_view(request, exception=None):
    return render(request, "main/error.html", {"error": "404: Strona nie odnaleziona"}, status=404)


def custom_error_view(request, exception=None):
    return render(request, "main/error.html", {"error": "500: Błąd views"})


def custom_permission_denied_view(request, exception=None):
    return render(request, "main/error.html", {"error": "403: Brak permisji"})


def custom_bad_request_view(request, exception=None):
    return render(request, "main/error.html", {"error": "400: Zły request"})

