
from django import forms
from shop.models import userShippingDetail,userDetails
from django.forms import ModelForm



class userdetailForm(forms.Form):

    username=forms.CharField(max_length="40", required=True, help_text="Enter a valid username! ")
    password1=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())
    email=forms.EmailField(max_length="40",required=True,help_text="Enter a valid email! ")
    first_name=forms.CharField(max_length="50",required=True)
    last_name=forms.CharField(max_length="50",required=True,)
    address=forms.CharField(max_length="100",required=True,help_text="Enter a address! ")
    mobile=forms.IntegerField(required=True,help_text="Enter a valid number! ")

class userShippingForm(forms.Form):
    City=(
    ('Indore','Indore'),('Bhopal','Bhopal'),('Mumbai','Mumbai'),('Banglore','Banglore'),('Delhi','Delhi'),
    ('Rewa','Rewa'),)
    Country=(
        ("India","India"),
    )
    #username=forms.CharField(max_length=100,label="username", widget=forms.TextInput(attrs={'readonly':'readonly'}))
    name=forms.CharField(max_length=100,label="name", widget=forms.TextInput(),required=True)
    email=forms.EmailField(max_length=100, label="Email", required=True)
    city=forms.ChoiceField(choices=City,required=True, label="choose your city")
    pincode=forms.IntegerField(label="enter your pincode", required=True)
    country=forms.ChoiceField(choices=Country,label="choose your country", required=True)
    address=forms.CharField(label="Enter your address", widget=forms.Textarea(), required=True)
    mobile=forms.IntegerField(label="Enter your mobile number",required=True)


class updateProfileForm(forms.Form):
    profilePhoto=forms.ImageField(required=False, label="Update your profile picture")
    firstname=forms.CharField(label="Update Your first name",max_length=200,widget=forms.TextInput(),required=False)
    lastname=forms.CharField(label="Update Your last name",max_length=200,widget=forms.TextInput(),required=False)
    email=forms.EmailField(label="Update your email", max_length=200,widget=forms.EmailInput(),required=False)
    pincode=forms.IntegerField(label="Update Pincode",widget=forms.NumberInput(),required=False)
    address=forms.CharField(label="update your address",widget=forms.Textarea(),required=False)
    officeAddress=forms.CharField(label="update your office address",widget=forms.Textarea(),required=False)
    mobile=forms.IntegerField(label="Update Mobile",widget=forms.NumberInput(),required=False)
    alternateMobile=forms.IntegerField(label="Update alternate",widget=forms.NumberInput(),required=False)
