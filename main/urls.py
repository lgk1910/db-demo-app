from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:id>/', views.index, name='index'),
    path('', views.view_books, name='home'),
    path('home/', views.view_books, name='home'),
    path('insertcard/', views.insertCardInfo, name='insertcard'),
    path('view_books/', views.view_books, name='books'),
    path('p<str:isbn>/', views.product_detail, name='product_detail'),
    path('report/', views.report, name='report'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('finish_payment/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
    path('cc<str:isbn>/', views.change_cart, name='change_cart'),
    path('ri<str:isbn>/', views.remove_item_from_cart, name='remove_item_from_cart'),
]