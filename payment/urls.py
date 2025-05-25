from django.urls import path
from .views import *


urlpatterns = [
    path("get-cart-detail/", GetUserCartDetailView.as_view()),
    path("add-product-to-cart/", AddProductToCartView.as_view()),
]