from django.test import TestCase

# Create your tests here.
from django.test import Client
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem
from django.urls import reverse
from django.contrib.auth import get_user_model




# class CartTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
#         self.product = Product.objects.create(
#             name='Guarfia Heels Product',
#             price=1000,
#             category='Women',
#             subcategory='shoes',
#             description='Test description',
#             image='products/ws1.jpg',
#             stock=50
#         )
    
#     def test_add_to_cart(self):
#         self.client.login(username='testuser', password='testpass123')
#         response = self.client.post('/add_to_cart', {
#             'product_id': self.product.id,
#             'size': 'M'
#         })  

#         self.assertEqual(response.status_code, 200)
        
#         session = self.client.session
#         cart_items = session.get('cart', [])
#         self.assertEqual(len(cart_items), 1)

#         # verify product details  exists 
#         self.assertEqual(cart_items[0]['name'], 'Guarfia Heels Product')
#         self.assertEqual(cart_items[0]['price'], 1000)
#         self.assertEqual(cart_items[0]['size'], 'M')
#         self.assertEqual(cart_items[0]['description'], 'Test description')
#         self.assertEqual(cart_items[0]['image'], '/media/products/ws1.jpg')
#         self.assertEqual(cart_items[0]['quantity'], 1) 

#     def test_login_required(self):
#         response = self.client.get('/women')
#         self.assertEqual(response.status_code, 302)  # Redirect to login because view requires authentication



class LoginUserTestCase(TestCase):
    def setUp(self):
        self.client = Client() 
        self.login_url = reverse('login')
        self.index_url = reverse('index')
        self.user = User.objects.create_user(
            username='sammy',
            password='pass1'
        )
    
    # def test_login_page_get(self):
    #     response = self.client.get(self.login_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'shop/login.html')

    #     response = self.client.post(self.login_url, {
    #         'username': 'sammy',
    #         'password': 'pass1'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response['HX-Redirect'], self.index_url)

    def test_successful_login_with_next_param(self):
        next_url = reverse('women')
        response = self.client.post(f"{self.login_url}?next={next_url}", {
        'username': 'sammy',
        'password': 'pass1'
        })
        self.assertEqual(response['HX-Redirect'], next_url)
        
    def test_invalid_username(self):
        response = self.client.post(self.login_url, {
        'username': 'invaliduser',
        'password': 'testpass123'
        })
        self.assertContains(response, 'Invalid username')

    def test_invalid_password(self):
        response = self.client.post(self.login_url, {
        'username': 'sammy',
        'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid password')
    
    # def test_missing_fields(self):
    #     response = self.client.post(self.login_url, {
    #     'username': '',
    #     'password': 'testpass123'
    #     })
    #     self.assertContains(response, 'Invalid username or password')

    #     response = self.client.post(self.login_url, {
    #     'username': 'testuser',
    #     'password': ''
    #     })

    # def test_login_session(self):
    #     self.client.post(self.login_url, {
    #     'username': 'sammy',
    #     'password': 'pass1'
    #     })
    #     response = self.client.get(self.index_url)

    #     self.assertEqual(response.context['user'].username, 'sammy')
