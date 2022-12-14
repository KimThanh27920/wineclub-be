# From django
from django.shortcuts import get_object_or_404
# From rest_framework
from rest_framework import generics, status, permissions, filters
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# From app
from .serializers import CouponOwnerReadSerializer, CouponListSerializer, CouponDetailSerializer
from ..models import Coupon, CouponOwner

 
 
class CouponOwnerCreateListView(generics.ListCreateAPIView):
    serializer_class = CouponListSerializer
    queryset = CouponOwner.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['type', 'created_by']
    ordering_fields = ['time_start', 'time_end', 'created_at']
    pagination_class = None
    
    def get_serializer_class(self):
        if(self.request.method == "GET"):
            self.serializer_class = CouponOwnerReadSerializer
        
        return super().get_serializer_class()
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(CouponOwner, account=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        get_object_or_404(Coupon, id=self.request.data.get("coupon_id"))
        obj_coupon = instance.coupons.filter(id=self.request.data.get("coupon_id"))
        if (obj_coupon.exists()):
            return Response(data={"message": "You have been added this coupon"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance.coupons.add(self.request.data.get("coupon_id"))
                     
        instance.save()        
        serializer = self.get_serializer(instance.coupons.last())       
           
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class CouponRemoveView(generics.RetrieveDestroyAPIView):
    serializer_class = CouponDetailSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "coupon_id"
    
    def get_object(self):
        # obj = CouponOwner.objects.get(account=self.request.user.id)
        obj = get_object_or_404(CouponOwner, account=self.request.user.id)
        return obj
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        coupon_id = self.kwargs['coupon_id']
        instance.coupons.remove(coupon_id)
        instance.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)