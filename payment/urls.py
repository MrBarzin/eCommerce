from django.urls import path
from .views import *


urlpatterns = [
    path("get-cart-detail/", GetUserCartDetailView.as_view()),
    path("add-product-to-cart/", AddProductToCartView.as_view()),
    path("cart-detail-view/", CartDetailView.as_view()),
    path("delete-cart-item-api/<int:pk>/", DeleteCartItemAPIView.as_view()),
    path("update-cart-item-quantity-api/<int:pk>/", UpdateCartItemQuantityAPIView.as_view())
]