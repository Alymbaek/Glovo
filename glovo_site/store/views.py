from rest_framework import viewsets, generics, permissions,status
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .permissions import CheckCourier, CheckReview, CheckOwner,CheckOrder, StoreOwner,Couriercheck,CourierOwn
from .filters import StoreFilter

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken




class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class StoreListViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckCourier, CheckOwner, StoreOwner]



class StoreDetailViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StoreFilter
    permission_classes = [permissions.IsAuthenticated, CheckCourier, CheckOwner, StoreOwner]



class OrderListAPIViewt(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOrder]




class OrderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, CheckOrder]


class ReviewStoreListApiView(generics.ListCreateAPIView):
    queryset = ReviewStore.objects.all()
    serializer_class = ReviewStoreSerializer
    permission_classes = [permissions.IsAuthenticated, CheckReview]



class ReviewStoreRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ReviewStore.objects.all()
    serializer_class = ReviewStoreSerializer
    permission_classes = [permissions.IsAuthenticated, CheckReview]


class ReviewCourierListApiView(generics.ListCreateAPIView):
    queryset = ReviewCourier.objects.all()
    serializer_class = ReviewCourierSerializer
    permission_classes = [permissions.IsAuthenticated, CheckReview, CourierOwn]





class ReviewCourierRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ReviewCourier.objects.all()
    serializer_class = ReviewCourierSerializer
    permission_classes = [permissions.IsAuthenticated, CheckReview, CourierOwn]

class CourierListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourierSerializer
    permission_classes = [permissions.IsAuthenticated, Couriercheck]

    def get_queryset(self):
        return Courier.objects.filter(user_courier=self.request.user)




class CourierRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [permissions.IsAuthenticated, Couriercheck]

    def get_queryset(self):
        return Courier.objects.filter(user_courier=self.request.user)




class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)



