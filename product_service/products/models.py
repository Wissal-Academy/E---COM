from django.db import models
from django.contrib.auth import get_user_model

import uuid

User = get_user_model()


class APIToken(models.Model):
    """
        Model top store custom API TOKEN for users
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} :: Token : {self.token}'


class Category(models.Model):
    name = models.CharField('name', max_length=100)
    description = models.TextField('description', blank=True)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
