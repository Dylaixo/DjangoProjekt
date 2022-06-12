from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='citys', blank=True)
#    image = models.ImageField(upload_to='media', blank=True)

    def __str__(self):
        return self.name


class Attractions(models.Model):
    name = models.CharField(max_length=200)
    time = models.PositiveSmallIntegerField(help_text="czas podany w minutach")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
#    image = models.ImageField(upload_to, blank=True)
    image = models.ImageField(upload_to='attractions', blank = True)
    price = models.PositiveIntegerField(default=0)
    desc = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)


    def __str__(self):
        return self.name


class Cart(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    attractions = models.ManyToManyField(Attractions, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField()
    first_attraction = models.ForeignKey(Attractions, null=True, on_delete=models.CASCADE,
                                         related_name="first_attraction")
    last_attraction = models.ForeignKey(Attractions, null=True, on_delete=models.CASCADE,
                                         related_name="last_attraction")
    distance = models.CharField(max_length=1000, blank=True, null=True)
