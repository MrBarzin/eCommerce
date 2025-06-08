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
        
        
        
class CartDetailView(TemplateView):
    template_name = "payment/cart_detail.html"
    
    def get_context_data(self, **kwargs):
        return {}
    
    
    
class DeleteCartItemAPIView(drf_generics.DestroyAPIView):
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)



    
class UpdateCartItemQuantityAPIView(drf_generics.UpdateAPIView):
    serializer_class = UpdateCartItemQuantitySerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def patch(self, request, *args, **kwargs):
        response =  super().patch(request, *args, **kwargs)
        item: CartItem = self.get_object()
        print(item.quantity)
        if item.quantity < 1:
            item.delete()
        return response
    

class CreateOrderAPIView(drf_generics.GenericAPIView):
    permission_classes = [drf_perms.IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        if not cart.cart_items.exists():
            return Response(data={"error": "There is any item in the user cart."}, status=400)
        
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        shipping_address = serializer.validated_data.get("shipping_address")

        order = Order.objects.create(
            user=self.request.user,
            total_amount = cart.total_price,
            shipping_address =shipping_address
        )
        
        for cart_item in cart.cart_items.all():            
            OrderItem.objects.create(
                order = order,
                product = cart_item.product,
                quantity = cart_item.quantity,
                price = cart_item.total_price,
            )
            cart_item.delete()
        serializer = OrderDetailSerializer(instance=order)   
        return Response(data=serializer.data, status=201)
    
    
class OrdersListView(TemplateView):
    template_name = "payment/orders_list.html"
    
    def get_context_data(self, **kwargs):
        return {"orders": Order.objects.filter(user=self.request.user)}