from django.contrib.auth.models import User
from django.test import TestCase
from .models import Cart, Attractions, City, Category
import random


class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.login(username='test', password='test123')
        self.cart = Cart.objects.create(user=self.user, completed=False)
        self.city = City.objects.create(name="test")
        self.attractions_list = []
        self.category = Category.objects.create(name="test")
        for i in range(0, 10):
            attraction = Attractions.objects.create(
                name=str(i),
                time=random.randint(1, 100),
                category=self.category,
                price=random.randint(1, 100),
                desc="test",
                city=self.city,
                lat=random.uniform(50.5, 52.5),
                long=random.uniform(50.5, 52.5)
            )
            self.attractions_list.append(attraction)
            self.cart.attractions.add(attraction)
        self.cart.first_attraction = self.attractions_list[0]
        self.cart.last_attraction = self.attractions_list[len(self.attractions_list) - 1]

    def test_cart_empty_view(self):
        self.cart.completed = True
        self.cart.save()
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/cart_empty.html")
        self.cart.completed = False
        self.cart.save()

    def test_cart_view(self):
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/cart.html")

    def test_profile_view(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/profile.html")
        self.assertContains(response, '<h2>Aktualny plan:</h2>\n    <a href="/cart">\n    <h3>test</h3>\n')

    def test_attraction_view(self):
        attraction = Attractions.objects.get(id=random.randint(1,10))
        response = self.client.get(f'/attractions/single_attraction/{attraction.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/single_attraction.html")
        self.assertContains(response, f'{attraction.price}')
        self.assertContains(response, f'{attraction.time}')
        self.assertContains(response, f'{attraction.city.name}')

    def test_attraction_add_view(self):
        attraction = Attractions.objects.get(id=random.randint(1, 10))
        self.cart.attractions.remove(attraction)
        response = self.client.get(f'/attractions/single_attraction/{attraction.id}/add')
        self.assertRedirects(response, f'/attractions/single_attraction/{attraction.id}', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertIn(attraction, self.cart.attractions.all())
