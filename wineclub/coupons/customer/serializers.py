# From django
from django.contrib.auth import get_user_model
# From rest_framework
from rest_framework import serializers
# From app
from wineries.models import Winery
from ..models import Coupon, CouponOwner

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
 
 
class CouponListSerializer(serializers.ModelSerializer):
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
            "description",
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
            "description",
            "image",
            "title",
            "time_start",
            "time_end",    
            "created_by", 
        ]
    
    def to_representation(self, instance):
        limit_content = instance.description
        if len(limit_content) > 100:
            limit_content = limit_content[:100]
            instance.description = limit_content
            instance.description += "..."
    
        return super().to_representation(instance)
    
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
            "individual",
            "currency",
            "image",
            "title",
            "description",
            "coupon_amount",
            "time_start",
            "time_end",    
            "created_by",  
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
        ]


class CouponOwnerReadSerializer(serializers.ModelSerializer):
    coupons = CouponListSerializer(many=True)
    class Meta:
        model = CouponOwner
        fields = [
            "coupons"
        ]