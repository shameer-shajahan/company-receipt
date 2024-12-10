from django.db import models

from django.contrib.auth.models import AbstractUser 


# Create your models here.

class User(AbstractUser):

    phone=models.CharField(max_length=15,unique=True)

class DeliveryReceipt(models.Model):

    receipt_number = models.CharField(max_length=100)

    date = models.DateField(auto_now_add=True)

    company_name = models.CharField(max_length=200)

    company_address = models.TextField()

    email = models.EmailField()

    phone_number = models.CharField(max_length=15)

    logo=models.ImageField(upload_to="commpont_logo",null=True,blank=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):

        return self.receipt_number
    

class Item(models.Model):

    receipt = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    serial_number = models.IntegerField()

    item_description = models.CharField(max_length=255)

    quantity = models.IntegerField()

    uom = models.CharField(max_length=50)

    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
       
        return f"Item {self.serial_number} for {self.receipt.receipt_number}"
    
    