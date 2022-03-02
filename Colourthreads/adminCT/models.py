
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE


# Create your models here.
def validate_phone_number(value):
    if len(value)==10:
        return value
    else:
        raise ValidationError("Enter a valid phone number")


def get_stock_image_filepath(self, filename):
    DirectoryPath = f"media/{self.sid}/ProfilePicture/.jpg"
    return DirectoryPath

def get_default_stock_image():
    return "media/default.jpeg"

class Stocks(models.Model):
    sid=models.AutoField(primary_key=True)
    sname=models.CharField(max_length=255)
    scategory=models.CharField(max_length=255)
    #image=models.ImageField(upload_to=get_stock_image_filepath, default=get_default_stock_image)
    sqty=models.IntegerField()
    sprice=models.FloatField()
    sdescription=models.TextField()
    class Meta :
        db_table="Stocks"
    def save(self, *args, **kwargs):
        self.sprice = round(self.sprice, 2)
        super(Stocks, self).save(*args, **kwargs)
    

class AdminCT(models.Model):
    A_id =models.AutoField(primary_key=True)
    A_name=models.CharField(null=False,max_length=100)
    A_email=models.EmailField(unique=True,max_length=255)
    A_password=models.CharField(null=False,max_length=255)
    A_phonenumber=models.CharField(max_length=10,validators =[validate_phone_number])
    isAuthenticated=models.BooleanField()
    last_login=models.CharField(max_length=255)
    class Meta:
        db_table="AdminCT"

class Customers(models.Model):
    cid =models.AutoField(primary_key=True)
    cname=models.CharField(null=False,max_length=75)
    cemail=models.EmailField(unique=True,max_length=255)
    cpassword=models.CharField(null=False,max_length=255)
    isAuthenticated = models.BooleanField()
    last_login=models.CharField(max_length=255)
    class Meta:
        db_table="Customers" 


class cust_phone_number(models.Model):
    id = models.AutoField(primary_key=True)
    customerid=models.ForeignKey(Customers,on_delete=CASCADE)
    phone_number = models.CharField(max_length=10,validators =[validate_phone_number])
    class Meta:
        db_table="Cust_phone_number"
        

class cust_address(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.ForeignKey(Customers,on_delete=CASCADE)
    address1=models.CharField(max_length=255,null=True)
    address2=models.CharField(max_length=255,null=True)
    city=models.CharField(max_length=75,null=True)
    zipcode=models.CharField(max_length=10,null=True)
    class Meta:
        db_table="Cust_address"

class Wishlist(models.Model):
    id=models.AutoField(primary_key=True)
    cid=models.IntegerField()
    sid=models.IntegerField()
    class Meta:
        db_table="Wishlist"

class CART(models.Model):
    id=models.AutoField(primary_key=True)
    cid=models.IntegerField()
    sid=models.IntegerField()
    class Meta:
        db_table="CART"

class Orders(models.Model):
    id=models.AutoField(primary_key=True)
    cid=models.IntegerField()
    sid=models.IntegerField()
    class Meta:
        db_table="Orders"










