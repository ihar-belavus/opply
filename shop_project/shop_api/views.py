from django.contrib.auth import get_user_model, login

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveDestroyAPIView, ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from shop_api.models import (
    Product,
    Order
)
from shop_api.serializers import (
    ProductSerializer,
    OrderSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenSerializer
)

User = get_user_model()


@extend_schema(tags=["User"])
class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer


@extend_schema(tags=["User"])
class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response(
                data={"token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(tags=["User"])
class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)


@extend_schema(tags=["Products"])
class ProductListAPIView(ListAPIView):
    """
        API endpoint for listing products.
    """
    serializer_class = ProductSerializer
    permission_classes = ()

    def get_queryset(self):
        return Product.objects.all()


@extend_schema(tags=["Products"])
class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


@extend_schema(tags=["Orders"])
class OrderListAPIView(ListAPIView):
    """
        API endpoint for listing orders.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.id)


@extend_schema(tags=["Orders"])
class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
