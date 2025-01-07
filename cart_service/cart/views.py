import requests
from decimal import Decimal

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Cart.objects.filter(user=self.request.user)

    def get_product_details(self, product_id):
        response = requests.get(
            f'http://localhost:8001/api/products/{product_id}'
        )
        if response.status_code == 200:
            """
            {
                "id": 1,
                "name": "clavier razor",
                "price": 299
                ...
            }
            """
            return response.json()
        return None

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Call the Product Service using the top function
        product = self.get_product_details(product_id)
        if not product:
            return Response(
                {
                    'error': 'Product not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"price": Decimal(str(product['price']))}
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')

        try:
            item = cart.items.get(id=item_id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
