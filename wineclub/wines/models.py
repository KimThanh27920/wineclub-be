#django import
from django.db import models
from django.contrib.auth import get_user_model

# App import
from categories.models import Style, Type, Grape, Food, Region, Country 

User = get_user_model()


# Style model class
class Style(models.Model):
    wine = models.CharField(max_length=255, unique=True)
    price = models.FloatField(),

    #winery = models.ForeignKey(Winery, on_delete=models.CASCADE, related_name="origin")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="type_wine")
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="style_wine")
    grape = models.ForeignKey(Grape, on_delete= models.CASCADE, related_name="grape_wine")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="food_pairing")
    region = models.ForeignKey(Region,on_delete=models.CASCADE, related_name="region_wine")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_wine")
    
    thumbnail = models.CharField(max_length=255)
    year = models.IntegerField()
    descriptions = models.TextField()
    alcohol = models.FloatField()
    bottle_per_case = models.IntegerField()
    net = models.IntegerField()
    serving_temprature = models.FloatField()
    in_stock = models.IntegerField()
    
    light_bold = models.FloatField()
    smooth_tannic = models.FloatField()
    dry_sweet = models.FloatField()
    soft_acidic = models.FloatField()

    average_rating = models.FloatField()
    reviewers = models.IntegerField
    is_active = models.BooleanField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wine_created")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wine_updated")
    deleted_by = models.ForeignKey(User, on_delete= models.CASCADE, related_name="wine_deleted")
