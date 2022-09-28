from rest_framework import serializers

from django.contrib.auth import get_user_model

from wineries.models import Winery
from ..models import Coupon

User = get_user_model()
    
    
    
class CouponWriteUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Coupon
        fields = [
            "is_active",         
        ]
    

class WinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Winery
        fields = [
            "id",
            "name"
        ]      
 
 
class AccountSerializer(serializers.ModelSerializer):
    wineries = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = [
            "wineries",
            "email",
            "image",        
        ]

    
class CouponReadSerializer(serializers.ModelSerializer):
    created_by = AccountSerializer(read_only=True)
    updated_by = AccountSerializer(read_only=True)
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
            "individual",
            "currency",
            "image",
            "title",
            "description",
            "coupon_amount",
            "time_start",
            "time_end",
            "is_public",
            "is_active",   
            "created_at",
            "created_by",
            "updated_at",           
            "updated_by", 
        ]
        read_only_fields = [
            "code",
            "type",
            "type_reduce",
            "coupon_value",
            "max_value",
            "min_order_value",
            "individual",
            "currency",
            "image",
            "title",
            "description",
            "coupon_amount",
            "time_start",
            "time_end",
            "is_public",
            "is_active",   
            "created_at",
            "created_by",
            "updated_at",          
            "updated_by",   
        ]