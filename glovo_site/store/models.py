from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    ROLE_CHOICES = (
        ('courier','courier'),
        ('client', 'client'),
        ('ownerUser', 'ownerUser'),

    )
    role = models.CharField(max_length=35, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return f'{self.username} - {self.role}'

class Store(models.Model):
    store_name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    contact_info = PhoneNumberField(null=True, blank=True, region='KG')
    address = models.CharField(max_length=35)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image_store = models.ImageField(upload_to='images_store')

    def __str__(self):
        return self.store_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.rating_store for rating in ratings) / ratings.count(), 1)
        return 0

    def get_total_ratings(self):
        reviews = self.ratings.all()
        if reviews.exists():
            if reviews.count() > 1:
                return '1+'
            else:
                return reviews.count()
        return 0

    def get_total_percent(self):
        ratings = self.ratings.all()  # Получаем все оценки
        if ratings.exists():
            tot = len(ratings) * 5
            san1 = ratings.count(4)
            koboy = san1 * 100 / tot

            return koboy
        return 0




class Product(models.Model):
    product_name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveSmallIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product')
    image_product = models.ImageField(upload_to='images_product')

    def __str__(self):
        return f'{self.store.store_name} - {self.product_name}'

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, related_name='cart', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        return total_price

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=35)
    courier = models.ForeignKey(UserProfile, related_name='order_courier', on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client.username} - {self.cart_item.product.product_name}'


class Courier(models.Model):
    user_courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='courier_current', null=True, blank=True)
    STATUS = (
        ('Ожидает обработки', 'Ожидает обработки'),
        ('В процессе доставки', 'В процессе доставки'),
        ('Доставлен', 'Доставлен'),
        ('Отменен ', 'Отменен'),

    )
    status = models.CharField(max_length=75, choices=STATUS)


    def __str__(self):
        return f'{self.user_courier}'

    def get_average_rating(self):
        ratings = self.rating.all()
        if ratings.exists():
            return round(sum(ratings.rating_courier for ratings in ratings) / ratings.count(), 1)
        return 0

    def get_total_courier_ratings(self):
        reviews = self.rating.all()
        if reviews.exists():
            if reviews.count() > 100:
                return '100+'
            else:
                return reviews.count()
        return 0







class ReviewStore(models.Model):
    store_client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    rating_store = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)], verbose_name='Рейтинг', null=True, blank=True)
    comment_store = models.TextField(null=True, blank=True)




class ReviewCourier(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True, related_name='rating')
    rating_courier = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)], verbose_name='Рейтинг', null=True, blank=True)
    comment_courier = models.TextField(null=True, blank=True)













