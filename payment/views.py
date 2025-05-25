import uuid

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.core.mail import send_mail

from rest_framework import generics as drf_generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions as drf_perms
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *


class GetUserCartDetailView(drf_generics.GenericAPIView):
    serializer_class = GetCartDetailSerializer
    permission_classes = [drf_perms.IsAuthenticated]
    
    def get(self, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(instance=cart)
        return Response(data=serializer.data, status=200)
    
    
class AddProductToCartView(drf_generics.GenericAPIView):
    serializer_class = AddProductToCartSerializer
    permission_classes = [drf_perms.IsAuthenticated]
    
    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        product = serializer.validated_data.get("product")
        quantity = serializer.validated_data.get("quantity")
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity += (quantity - 1)
        else:
            cart_item.quantity = cart_item.quantity + quantity
            
        cart_item.save()
        
        return Response({"detail": "Product added successfully."}, status=status.HTTP_200_OK)
        