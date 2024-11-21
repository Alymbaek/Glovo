from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role',
                  'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'role']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username', 'first_name', 'last_name', 'role']


class StoreListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'image_store', 'store_name', 'description', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'image_product', 'product_name', 'description', 'price', 'quantity']

class StoreDetailSerializer(serializers.ModelSerializer):
    owner = UserProfileListSerializer()
    product = ProductListSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'image_store', 'store_name', 'average_rating', 'product',
                  'address', 'owner', 'description', 'contact_info']

    def get_average_rating(self, obj):
        return obj.get_average_rating()




class ReviewStoreSerializer(serializers.ModelSerializer):
    store_client = UserProfileListSerializer()
    store = StoreListSerializer()
    class Meta:
        model = ReviewStore
        fields = ['id', 'store_client', 'store', 'rating', 'comment']

class CourierSimpleSerializer(serializers.ModelSerializer):
    user_courier = UserProfileListSerializer()
    class Meta:
        model = Courier
        fields = ['user_courier', 'status']

class ReviewCourierSerializer(serializers.ModelSerializer):
    client = UserProfileListSerializer()
    courier = CourierSimpleSerializer()

    class Meta:
        model = ReviewCourier
        fields = ['id', 'client', 'courier', 'rating', 'comments']

class OrderSerializer(serializers.ModelSerializer):
    client = UserProfileListSerializer()
    products = ProductListSerializer()
    courier_current = CourierSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'products', 'delivery_address',
                  'courier_current', 'created_at']


class CourierSerializer(serializers.ModelSerializer):
    current_orders = OrderSerializer()
    average_rating = serializers.SerializerMethodField()
    user_courier = UserProfileListSerializer()
    class Meta:
        model = Courier
        fields = ['id','average_rating', 'user_courier', 'current_orders', 'status']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'get_total_price']





class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


























