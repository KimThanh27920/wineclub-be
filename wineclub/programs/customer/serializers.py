# From django
from django.contrib.auth import get_user_model
# From rest_framework
from rest_framework import serializers
# From app
from programs.models import RewardProgram
from coupons.models import Coupon
from wineries.models import Winery

User = get_user_model()



class WinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Winery
        fields = [
            "id",
            "name"
        ]      

 
class AccountSerializer(serializers.ModelSerializer):
    wineries = WinerySerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            "wineries",
            "email",
            "image",        
        ]


class CouponDetailSerializer(serializers.ModelSerializer):
    created_by = AccountSerializer(read_only=True)
    class Meta: 
        model = Coupon
        fields = [
            "id",
            "code",
            "type",
            "type_reduce",
            "coupon_value",
            "max_value",
            "min_order_value",
            "currency",
            "image",
            "title",
            "time_start",
            "time_end",    
            "created_by", 
        ]
        read_only_fields = [
            "id",
            "code",
            "type",
            "type_reduce",
            "coupon_value",
            "max_value",
            "min_order_value",
            "currency",
            "image",
            "title",
            "time_start",
            "time_end",    
            "created_by", 
        ]
    

class RewardProgramReadDetailSerializer(serializers.ModelSerializer):
    coupons = CouponDetailSerializer(read_only=True, many=True)
    message = serializers.CharField(max_length=255)
    class Meta:
        model = RewardProgram
        fields =[
            'message',
            'coupons',
        ]
        
        read_only_fields = [
            'message',
            'coupons',
        ]