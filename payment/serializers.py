from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ("title", "description", "stock", "price", "slug", "image")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class GetCartDetailSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("user", "cart_items")
        
        
class AddProductToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.all())
    quantity = serializers.IntegerField()
    
    def validate_quantity(self, data):
        if data < 1:
            serializers.ValidationError("Quantity must be positive.")
        return data


class UpdateCartItemQuantityAPIView(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity",)