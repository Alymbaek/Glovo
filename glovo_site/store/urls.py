from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'store', StoreListViewSet, basename='store-list'),
router.register(r'store-detail', StoreDetailViewSet, basename='store-detail'),



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),

    path('', include(router.urls)),

    path('user/', UserProfileListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-detail'),

    path('orders/', OrderListAPIViewt.as_view(), name='orders-llist'),

    path('review-store/', ReviewStoreListApiView.as_view(), name='review_store-list'),
    path('review-store/<int:pk>/', ReviewStoreRetrieveDestroyAPIView.as_view(), name='review_store-detail'),

    path('review-courier/', ReviewCourierListApiView.as_view(), name='review_courier-list'),
    path('review-courier/<int:pk>/', ReviewCourierRetrieveDestroyAPIView.as_view(), name='review_courier-detail'),

    path('courier/', CourierListCreateAPIView.as_view(), name='courier-list'),
    path('courier/<int:pk>/', CourierRetrieveUpdateAPIView.as_view(), name='courier-detail'),

    path('cart/', CartViewSet.as_view({'get': 'retrieve'}), name='cart_detail'),

    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart_item_list'),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

]
