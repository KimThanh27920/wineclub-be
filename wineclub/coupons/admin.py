from django.contrib import admin

from .models import Coupon, CouponOwner
# Register your models here.


admin.site.register(Coupon)
admin.site.register(CouponOwner)
