from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

import random
import string

SizeOPTIONS = ((0, 'XS'), (1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL'))
ConditionOPTIONS = ((0, 'Ragged'), (1, 'Worn'), (2, 'Great'), (3, 'Band new'))
CategoryOPTIONS = ((0, 'Headwear'), (1, 'Tops'), (2, 'Trousers'), (3, 'Shoes'))
BrandOPTIONS = ((0, 'Other'), (1, 'Nike'), (2, 'Adidas'), (3, 'GUCCI'))
GenderOPTIONS = ((0, 'Male'), (1, 'Female'), (2, 'Unisex'))
UserTypeOPTIONS = (('STORE', 'STORE'), ('FEATURED', 'FEATURED'), ('USER', 'USER'))
LocationOPTIONS = ((0, 'Stockholm'), (1, 'Malmoe'), (2, 'Gothenburg'))

def create_product_slug():
    length = 40

    while True:
        slug = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Product.objects.filter(slug=slug).count() == 0:
            break
    return slug

def create_profile_slug():
    length = 40

    while True:
        slug = ''.join(random.choices(string.ascii_uppercase, k=length))
        if UserProfile.objects.filter(slug=slug).count() == 0:
            break
    return slug

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=20, default="")
    slug = models.SlugField(max_length=40, default=create_product_slug, unique=True)
    shoppingcarted = models.ManyToManyField(User, related_name="product_shoppingcarted", blank=True)
    liked = models.ManyToManyField(User, related_name="product_likes", blank=True)
    condition = models.IntegerField(choices=ConditionOPTIONS, default=0)
    
    sold_by = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    size = models.IntegerField(choices=SizeOPTIONS, default=0)
    gender = models.IntegerField(choices=GenderOPTIONS, default=0)
    brand = models.IntegerField(choices=BrandOPTIONS, default=0)
    category = models.IntegerField(choices=CategoryOPTIONS, default=0)
    user_type = models.CharField(max_length=20, choices=UserTypeOPTIONS, default='USER')
    prize = models.IntegerField(default="0")
    date_added = models.DateTimeField(auto_now_add=True)
    product_img = CloudinaryField('image', default='placeholder')

    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    username = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=40, default=create_profile_slug, unique=True)
    profile_pic = CloudinaryField('image', default='placeholder')
    description = models.TextField(default='')
    location = models.IntegerField(choices=LocationOPTIONS, default=0)
    follows = models.ManyToManyField(User, related_name="follower", blank=True)
    products_for_sale = models.ManyToManyField(Product, related_name="for_sale", blank=True)
    
    def __str__(self):
        return str(self.username)




