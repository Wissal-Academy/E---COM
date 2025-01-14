from rest_framework import serializers
from .models import Product, Category, APIToken


class APITokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIToken
        fields = ['name']

    def create(self, validate_data):
        # TAKE THE USER FROM THE REQUEST
        user = self.context['request'].user
        return APIToken.objects.create(user=user, **validate_data)


class APITokenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIToken
        fields = ['id', 'name', 'token', 'create_at', 'is_active']


class APITokenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIToken
        fields = ['is_active']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
        )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'category_name'
        ]
