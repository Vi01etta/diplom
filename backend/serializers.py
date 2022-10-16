from rest_framework import serializers

from .models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'apartment', 'e_mail', 'user', 'phone', 'work_phone',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'type', 'contacts')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    contact = ContactSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    state = serializers.CharField(source='get_state_display')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'dt', 'state', 'contact',
                  'shop', 'items', 'total_summ')
        read_only_fields = ('id',)
