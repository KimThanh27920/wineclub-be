#django import
from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth import get_user_model

# App import
from categories.models import Style, Type, Grape, Food, Region, Country 
from wineries.models import Winery
from bases.models import BasicLogModel

User = get_user_model()

WINE_STATUS = [
    (None,None),
    ("Block","Block"),
]
# Style model class
class Wine(BasicLogModel):
    wine = models.CharField(max_length=255)
    price = models.FloatField()
    sale = models.FloatField(null=True, blank=True, default=0)
    winery = models.ForeignKey(Winery, on_delete=models.CASCADE, related_name="origin")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="type_wine")
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="style_wine")
    grape = models.ForeignKey(Grape, on_delete= models.CASCADE, related_name="grape_wine")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="food_pairing")
    region = models.ForeignKey(Region,on_delete=models.CASCADE, related_name="region_wine")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_wine")
    thumbnail = models.ImageField(null=True, upload_to = "images/wine/thumbnails/")
    year = models.IntegerField()
    descriptions = models.TextField()
    alcohol = models.FloatField()
    bottle_per_case = models.IntegerField()
    net = models.IntegerField()
    serving_temperature = models.IntegerField()
    in_stock = models.IntegerField()
    
    #taste of wine
    light_bold = models.IntegerField()
    smooth_tannic = models.IntegerField()
    dry_sweet = models.IntegerField()
    soft_acidic = models.IntegerField()

    #rating of wine
    average_rating = models.FloatField(default=0)
    reviewers = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default= False)
    is_block = models.BooleanField(default= False)

    status = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table="wines"
        unique_together = ['wine', 'created_by']

    def __str__(self) -> str:
        return self.wine
    
