import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    STATUS_CHOICES = (
        # (DB_VALUE, APP_VIEW)
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed")
    )

    CIB = "CIB"
    CCP = "CCP"

    PAYMENT_METHOD = (
        (CIB, "CIB"),
        (CCP, "Baridi MOB")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    payment_method = models.CharField(
        max_length=200,
        choices=PAYMENT_METHOD,
        default=CCP
    )
    transaction_id = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
