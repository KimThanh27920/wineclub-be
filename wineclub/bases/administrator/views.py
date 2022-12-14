# rest framework import
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

# Python imports
# from datetime import datetime
from django.utils import timezone


#Base Admin Viewset
class BaseAdminViewset(ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_serializer_class(self):
        return self.serializer_class[self.action]

    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at__isnull=False).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user,
                        created_by=self.request.user)
                        
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save()
    