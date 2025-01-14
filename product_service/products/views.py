from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Category, Product, APIToken
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    APITokenCreateSerializer,
    APITokenListSerializer,
    APITokenUpdateSerializer
)


class APITokenGenerate(APIView):
    # IS AUTHENTICATED === USER IS CONNTECTED
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = APITokenCreateSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        if serializer.is_valid():  # CHECK IF DATA IS VALID
            token = serializer.save()  # SAVE TO DB
            return Response(
                {
                    'id': token.id,
                    'name': token.name,
                    'token': token.token,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
