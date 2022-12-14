# From django
from django.contrib.auth import get_user_model
# From rest_framework
from rest_framework import serializers
# From app
from ..models import Coupon

User = get_user_model()



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "is_staff"            
        ]


class CouponWriteSerializer(serializers.ModelSerializer):
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
            'type',
            "created_at",
            "created_by",
            "updated_at",           
            "updated_by",     
        ]
        
    def validate(self, attrs):
        if not(attrs['coupon_value'] > 0):
            raise serializers.ValidationError("Invalid coupon_value")
        
        if not(attrs['min_order_value'] > 0):
            raise serializers.ValidationError("Invalid min_order_value")
        
        if not(attrs['max_value'] > 0):
            raise serializers.ValidationError("Invalid max_value")
        
        if not(attrs['time_start'] < attrs['time_end']):
            raise serializers.ValidationError("Invalid time end before time start")
        
        return super().validate(attrs)
        
    def validate_coupon_amount(self, amount): #bd = birthday      
        if (not(0 < amount < 1000)):
            raise serializers.ValidationError("Invalid amount")
        
        return amount
    
class CouponWriteUpdateSerializer(serializers.ModelSerializer):
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
            "created_at",
            "created_by",
            "updated_at",           
            "updated_by",    
        ]
        
    def validate(self, attrs):
        if not(attrs['coupon_value'] > 0):
            raise serializers.ValidationError("Invalid coupon_value")
        
        if not(attrs['min_order_value'] > 0):
            raise serializers.ValidationError("Invalid min_order_value")
        
        if not(attrs['max_value'] > 0):
            raise serializers.ValidationError("Invalid max_value")
        
        if not(attrs['time_start'] < attrs['time_end']):
            raise serializers.ValidationError("Invalid time end before time start")
        
        return super().validate(attrs)
    
    def validate_coupon_amount(self, amount): #bd = birthday      
        if (not(0 < amount < 1000)):
            raise serializers.ValidationError("Invalid amount")
        
        return amount
 
    
class CouponUpdateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "image"
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
    
    def to_representation(self, instance):
        limit_content = instance.description
        if len(limit_content) > 100:
            limit_content = limit_content[:100]
            instance.description = limit_content
            instance.description += "..."
    
        return super().to_representation(instance)