from django.db import models
from owner.models import Books
from django.contrib.auth.models import User
from datetime import timedelta,datetime

# Create your models here.

class Cart(models.Model):
    product=models.ForeignKey(Books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
        ("incart","incart"),
        ("orderplaced","orderplaced"),
        ("ordercancelled","ordercancelled")
    )
    status=models.CharField(max_length=20,choices=options,default="incart")


class Orders(models.Model):
    product=models.ForeignKey(Books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=120)
    date=models.DateTimeField(auto_now_add=True)
    edate=datetime.today()+timedelta(days=5)
    expected_delivery_date = models.DateField(default=edate, null=True)
    options=(
        ("orderplaced","orderplaced"),
        ("dispatched","dispatched"),
        ("in_transit","in_transit"),
        ("delivered","delivered"),
        ("order_cancelled","order_cancelled")

    )
    status=models.CharField(max_length=20,choices=options,default="orderplaced")

