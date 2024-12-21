from django.urls import path
from .views import index, shop, blog, elements, register, login_view, product_list, cart_view, add_to_cart, cart_page

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('blog/', blog, name='blog'),
    path('elements/', elements, name='elements'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('products/', product_list, name='product_list'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/page/', cart_page, name='cart_page'),
]
