import requests

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=True, methods=['post'])
    def payment(self, request, pk=None):
        '''
            Body of the request
            {
                "cart_id": 1,
                "user": 1
            }
        '''
  
        try:
            cart_id = request.data.get('cart_id')
            # Check if the cart exists
            response = requests.get(
                f'http://127.0.0.1:8000/api/carts/{cart_id}/'
            )
            # Check if the response if cart exists
            if response.status_code == 200:
                # if the cart exists get the data into json
                cart_data = response.json()
                """
                "id": 1,
                    "user": 1,
                    "items": [
                        {
                            "id": 1,
                            "product_id": 1,
                            "quantity": 4,
                            "price": "2.92",
                            "subtotal": "11.68"
                        },
                    ...
                    ],
                    "total": "2323.60",
                    ...
                }
                """
                # Create a Payment Transaction
                payment = Payment.objects.create(
                    user=request.user,          # FOR THE USER ID
                    cart_id=cart_id,            # LINK THE CART TO THE PAYEMENT
                    amount=cart_data['total'],  # GET THE TOTAL OF THE CART
                    status=Payment.COMPLETED    # STATUS OF THE PAYMENT
                )
                payment.save()
                for item in cart_data['items']:
                    pk = item["product_id"]
                    qte = item["quantity"]
                    response = requests.get(
                        f'http://127.0.0.1:8001/api/products/{pk}/'
                    )
                    # ITEM DATA == PRODUCT GET
                    # QTE == CART
                    item_data = response.json()
                    new_qte = item_data["stock"] - qte
                    item_data.update({"stock": new_qte})
                    print(item_data, "<<<<<<<<<<<<<<<<<<<<<<<<")
                    requests.put(
                        f'http://127.0.0.1:8001/api/products/{pk}/',
                        item_data
                    )
                serializer = PaymentSerializer(payment)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'error': 'Failed to fetch the cart'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                    {
                        'error': f'{e}'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )


    @action(detail=True, methods=['post'])
    def retry_payment(self, rqeuest, pk=None):
        pass