#rest framework import
from rest_framework.response import Response
from rest_framework import status

#app imports
from wines.models import Wine 
from subscriptions.models import SubscriptionPackage


# check error of Wine
class CategoriesErrors:

    #check type have child 
    def type_has_child(type_id):
        if Wine.objects.filter(type=type_id).exists() :
            data={
                "success":False,
                "message": "Type has child data! "}
            return Response(data,status= status.HTTP_400_BAD_REQUEST)
    
    #check style already exist
    def style_has_child(style_id):
        if Wine.objects.filter(style=style_id).exists() :
            data={
                "success":False,
                "message": "Style has child data! "}
            return Response(data,status= status.HTTP_400_BAD_REQUEST)

    #check grape already exist
    def grape_has_child(grape):
        if Wine.objects.filter(grape=grape).exists() :
            data={
                "success":False,
                "message": "Grape has child data! "}
            return Response(data,status= status.HTTP_400_BAD_REQUEST)

    #check food already exist
    def food_has_child(food):
        if Wine.objects.filter(food=food).exists() :
            data={
                "success":False,
                "message": "Food has child data! "}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    
     #check region already exist
    def region_has_child(region):
        if Wine.objects.filter(region=region).exists() :
            data={
                "success":False,
                "message": "Region has child data! "}
            return Response(data,status= status.HTTP_400_BAD_REQUEST)
    
     #check country already exist
    def country_has_child(country):
        if Wine.objects.filter(country=country).exists() :
            data={
                "success":False,
                "message": "Country has child data! "}
            return Response(data,status= status.HTTP_400_BAD_REQUEST)


#SubscriptionCheck Errors
class SubscriptionPackageErrors:

    def exist(subs_pk_id):
        if not (SubscriptionPackage.objects.filter(id=subs_pk_id).exists()):
            data ={
                "success":False,
                "message": "Subscription Package don't exist or disable"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    def stripe_account_exist(stripe_account):
        if stripe_account is None:
            data ={
                "success":False,
                "message": "You don't have payment method"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)