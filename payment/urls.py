from django.urls import path
from .views import *

app_name = "payment"

urlpatterns = [
    path("get-cart-detail/", GetUserCartDetailView.as_view()),
    path("add-product-to-cart/", AddProductToCartView.as_view()),
    path("cart-detail-view/", CartDetailView.as_view(), name="cart-detail-view"),
    path("delete-cart-item-api/<int:pk>/", DeleteCartItemAPIView.as_view()),
    path("update-cart-item-quantity-api/<int:pk>/", UpdateCartItemQuantityAPIView.as_view()),
    path("create-order-api/", CreateOrderAPIView.as_view()),
    path("orders-list/", OrdersListView.as_view(), name="orders-list"),
]