from django.urls import path, include

from shop_api import views

app_name = 'shop_api'


products_patterns = [
    path(
        '',
        views.ProductListAPIView.as_view(),
        name='products-list'
    ),
    path('create/',
         views.ProductCreateAPIView.as_view(),
         name='products-create')
]

accounts_patterns = [
    path('', views.UserRegistrationAPIView.as_view(), name="registration"),
    path('login/', views.UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', views.UserTokenAPIView.as_view(), name="token"),
]
orders_patterns = [
    path(
        '',
        views.OrderListAPIView.as_view(),
        name='orders-list'
    ),
    path(
        'create/',
        views.OrderCreateAPIView.as_view(),
        name='orders-create'
    ),
]

urlpatterns = [
    path(
        'products/',
        include(products_patterns),
    ),
    path(
        'orders/',
        include(orders_patterns),
    ),
    path(
        'accounts/',
        include(accounts_patterns),
    )
]
