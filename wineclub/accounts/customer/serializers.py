from django.contrib.auth import get_user_model
from rest_framework import serializers
from addresses.models import Address
from datetime import date

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "phone",
            "type",
            "full_name",
            "is_default",
            "street",
            "ward",
            "district",
            "city",
            "country"
        ]


class ProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "full_name",
            "birthday",
            "gender",
            "points",
            "stripe_account",
            "image",
            "addresses"
        ]
        read_only_fields = [
            "points",
            "stripe_account",
            "email",
            "image"
        ]
        
    def validate_birthday(self, bd): #bd = birthday
        today = date.today()
        age = today.year - bd.year        
        if (not(0 < age < 150)):
            raise serializers.ValidationError("Invalid date of birth")
        
        return bd
    
    def validate_email(self, email):
        return email.lower()
    
    def validate_phone(self, attrs):
        try:             
            if not(len(attrs) == 10):
                raise serializers.ValidationError("Invalid phone number: Phone number have to include ten number")
            
            return attrs
        
        except:
            raise serializers.ValidationError("Invalid phone number: Don't include characters")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone",
            "full_name",
            "birthday",
            "gender",
            "image",
        ]
        
    def validate_birthday(self, bd): #bd = birthday
        today = date.today()
        age = today.year - bd.year        
        if (not(0 < age < 150)):
            raise serializers.ValidationError("Invalid date of birth")
        
        return bd
    
    def validate_email(self, email):
        return email.lower()
    
    def validate_phone(self, attrs):
        try:             
            if not(len(attrs) == 10):
                raise serializers.ValidationError("Invalid phone number: Phone number have to include ten number")
            
            return attrs
        
        except:
            raise serializers.ValidationError("Invalid phone number: Don't include characters")
    
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = [
           "old_password",
           "new_password",
           "confirm_password",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "image"
        ]