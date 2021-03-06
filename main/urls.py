
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('attractions', views.cities, name='cities'),
    path('attractions/<str:city>', views.attractions, name='attractions'),
    path('attractions/single_attraction/<int:id>', views.single_attraction, name='single_attraction'),
    path('attractions/single_attraction/<int:id>/add', views.add_attraction, name='add_attraction'),
    path('cart', views.cart, name='cart'),
    path('about', views.about, name='about'),
    path('profile', views.profile, name='profile'),
    path('cart/<int:id>', views.cart_show, name='cart_show')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

