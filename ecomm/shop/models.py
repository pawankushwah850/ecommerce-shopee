from django.db import models
from django.contrib.auth.models import User 
from ckeditor.fields import RichTextField

category=[
    ('Mobiles','Mobiles'),('Laptops','Laptops'),('Led','Led'),
    ('Books','Books'),('Toys','Toys'),('Accessories','Accessories'),
]
City=[
    ('Indore','Indore'),('Bhopal','Bhopal'),('Mumbai','Mumbai'),('Banglore','Banglore'),('Delhi','Delhi'),
    ('Rewa','Rewa'),
]

class orderStatus(models.Model):
    orderId=models.CharField(verbose_name="Order Id", max_length=200)
    razorpay_id=models.CharField(verbose_name="Razorpay Id",max_length=250)
    paymentStatus=models.BooleanField(verbose_name="Payment status",default=False)
    date=models.DateTimeField(auto_now_add=True,auto_created=True)


    def __str__(self):
        return self.orderId

# Create your models here.
class product(models.Model):
    productId=models.AutoField(primary_key=True)
    categoryType=models.CharField(max_length=40,blank=False,default='-',choices=category)
    productName=models.CharField(max_length=80,blank=False,help_text="Please enter product name")
    productDetails=RichTextField()
    productPrice=models.PositiveIntegerField(help_text="Please enter a price, in Rupees",blank=False)
    productImage=models.ImageField(upload_to="images/",blank=False)
    publishDate=models.DateTimeField(auto_now_add=True,auto_created=True)

    def __str__(self):
        return self.productName

class userDetails(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.PROTECT)
    ProfilePicture=models.ImageField(upload_to="userProfile/%Y/%m/%d/",blank=True,null=True)
    pinCode=models.PositiveIntegerField(help_text="Enter your area pincode!", blank=True,null=True)
    address=models.CharField(max_length=100, blank=False, help_text="Enter vaild address.")
    officeAddress=models.CharField(max_length=100,blank=True, help_text="enter your office address!..",null=True)
    mobile=models.PositiveIntegerField(blank=False,help_text="Enter valid number.")
    alternateMobile=models.PositiveIntegerField(blank=True, help_text="Enter your second number! in case your first nuber switchoff, we contact through this number",null=True)
    registrationDate=models.DateTimeField(auto_created=True,auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class userShippingDetail(models.Model):
    userID=models.ForeignKey(User,on_delete=models.CASCADE)
    orderId=models.OneToOneField(orderStatus, verbose_name="Order Id",on_delete=models.CASCADE)
    name=models.CharField(max_length=200,verbose_name='Buyer Name')
    email=models.EmailField(max_length=200,verbose_name="Email", null=False,blank=False)
    city=models.CharField(max_length=20,verbose_name="Buyer City",choices=City)
    pincode=models.PositiveIntegerField(verbose_name="Buyer city code")
    country=models.CharField(max_length=10,verbose_name="Buyer Country",choices=[("India","India"),])
    address=models.TextField(max_length=300,verbose_name="Buyer Full Address")
    mobile=models.PositiveIntegerField(verbose_name="Buyer Number")
    product=models.JSONField(verbose_name="Product In JSON type", blank=False,null=False)
    purchasedDate=models.DateTimeField(auto_now_add=True,auto_created=True)

    def __str__(self):
        return self.userID.username


class trackOrder(models.Model):
    
    orderId=models.OneToOneField(orderStatus,on_delete=models.CASCADE)
    stage1=models.CharField(max_length=200,verbose_name="stage 1",null=True,blank=True)
    stage2=models.CharField(max_length=200,verbose_name="stage 2",null=True,blank=True)
    stage3=models.CharField(max_length=200,verbose_name="stage 3",null=True,blank=True)
    stage4=models.CharField(max_length=200,verbose_name="stage 4",null=True,blank=True)
    stage5=models.CharField(max_length=200,verbose_name="stage 5",null=True,blank=True)
    stage6=models.CharField(max_length=200,verbose_name="stage 6",default="-",null=True,blank=True)
    stage7=models.CharField(max_length=200,verbose_name="stage 7",default="-",null=True,blank=True)
    delivery=models.DateField(verbose_name="Enter excepted date",null=True,blank=True)
    orderReceived=models.BooleanField(verbose_name="Order received",null=True,blank=True)
    orderReceivedDate=models.DateField(verbose_name="After receiving date",null=True,blank=True)

    def __str__(self):
        return self.orderId.orderId


    

