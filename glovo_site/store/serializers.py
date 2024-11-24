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


class UsersProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role']


class UsersProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'role']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'role']

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
        fields = ['id', 'image_product', 'product_name', 'description', 'price']



class ReviewStoreSerializer(serializers.ModelSerializer):
    store_client = UsersProfileListSerializer()
    store = StoreListSerializer()

    class Meta:
        model = ReviewStore
        fields = ['id', 'store_client', 'store', 'rating_store', 'comment_store']


class StoreDetailSerializer(serializers.ModelSerializer):
    owner = UsersProfileListSerializer()
    product = ProductListSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField()
    ratings = ReviewStoreSerializer(read_only=True, many=True)
    total_ratings = serializers.SerializerMethodField()
    total_percent = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'image_store', 'store_name', 'average_rating', 'total_ratings', 'total_percent', 'product',
                  'address', 'owner', 'description', 'contact_info', 'ratings']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_total_ratings(self, obj):
        return obj.get_total_ratings()

    def get_total_percent(self, obj):
        return obj.get_total_percent()




class CourierSimpleSerializer(serializers.ModelSerializer):
    user_courier = UsersProfileListSerializer()

    class Meta:
        model = Courier
        fields = ['user_courier', 'status']


class ReviewCourierSerializer(serializers.ModelSerializer):
    client = UsersProfileListSerializer()

    class Meta:
        model = ReviewCourier
        fields = ['id', 'client', 'courier', 'comment_courier']





class CartItemSimpleSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = ['product']


class OrderSerializer(serializers.ModelSerializer):
    courier_current = CourierSimpleSerializer(read_only=True, many=True)
    cart_item = CartItemSimpleSerializer()

    class Meta:
        model = Order
        fields = ['id', 'cart_item', 'delivery_address',
                  'courier_current', 'created_at']


class OrderSimpleSerializer(serializers.ModelSerializer):
    client = UsersProfileListSerializer()

    class Meta:
        model = Order
        fields = ['id', 'client', 'delivery_address']


class CourierSerializer(serializers.ModelSerializer):
    current_orders = OrderSerializer()
    average_rating = serializers.SerializerMethodField()
    user_courier = UsersProfileListSerializer()
    rating = ReviewCourierSerializer(read_only=True, many=True)
    total_courier_ratings = serializers.SerializerMethodField()

    class Meta:
        model = Courier
        fields = ['id', 'average_rating', 'user_courier', 'current_orders', 'rating', 'total_courier_ratings', 'status']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_total_courier_ratings(self, obj):
        return obj.get_total_courier_ratings()





class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    orders = OrderSerializer(read_only=True, many=True)

    class Meta:
        model = CartItem
        fields = ['product', 'orders', 'get_total_price', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()
    user = UsersProfileListSerializer()

    class Meta:
        model = Cart
        fields = ['user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
