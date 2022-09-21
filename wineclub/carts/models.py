from django.db import models
from django.contrib.auth import get_user_model

from wineries.models import Winery
from wines.models import Style
# Create your models here.

Account = get_user_model()


class Cart(models.Model):
    winery = models.ForeignKey(Winery, on_delete=models.CASCADE, related_name="winery_cart")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_cart")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField()

    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cart_updated")
    deleted_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cart_deleted")

    class Meta:
        unique_together = (("winery", "account"),)


class CartDetail(models.Model):
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_detail")
    wine = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="cartdetail")