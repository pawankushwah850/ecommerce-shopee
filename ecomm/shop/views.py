from django.shortcuts import render,redirect
from django.http import HttpResponse
from shop.models import product ,userDetails,userShippingDetail,orderStatus,trackOrder
import re,json
from shop.form import userdetailForm,userShippingForm,updateProfileForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from collections import defaultdict
import razorpay
import time,random

from django.core.mail import send_mail
from django.conf import settings
import smtplib, ssl

######################################################################

HOST_PORT=587
HOST_SERVER="smtp.gmail.com"
EMAIL_SENDER="pawankushwah850@gmail.com"
EMAIL_SENDER_PASSOWRD="P@wan7869"

######################################################################








# Create your views here.
def index(request):
    return render(request,"index.html")

def category(request,args):
    filterArgs=re.findall(r'[a-zA-Z]+',args)

    if filterArgs[0]:
        products=product.objects.all().filter(categoryType=str(filterArgs[0]))
        return render(request,"products_show.html",{'title':filterArgs[0],'productList':products})
    else:
        return HttpResponse("something went wrong....")

def signup(request):

    if request.method=="POST":
        form_data=userdetailForm(request.POST)

        if form_data.is_valid():
            new_username=form_data.cleaned_data.get('username')
            password1=form_data.cleaned_data.get('password1')
            password2=form_data.cleaned_data.get('password2')
            first_name=form_data.cleaned_data.get('first_name')
            last_name=form_data.cleaned_data.get('last_name')
            email=form_data.cleaned_data.get('email')
            address=form_data.cleaned_data.get('address')
            mobile=form_data.cleaned_data.get('mobile')

            if password1!=password2:
                    return render(request,'registration/signup.html',{'form' : userdetailForm()})
            else:

                try:
                    User.objects.get(username=new_username)
                    #return render(request,'registration/signup.html',{'form' : userdetailForm()})
                except User.DoesNotExist:
                    User.objects.create_user(username=new_username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user=authenticate(username=new_username,password=password2)
                    save_data=userDetails(address=address,mobile=mobile,user=user)
                    save_data.save()

                    '''
                    #sending mail
                    RECIVER_EMAIL= email
                    MESSAGE=f"""
                        subject : Thanking your for registring in our site

                        hey, {first_name} {last_name} , Welcome in our Myshopee.com.
                        Thanking you so much to registering in our site.

                        """

                    context = ssl.create_default_context()
                    with smtplib.SMTP(HOST_SERVER, HOST_PORT) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(EMAIL_SENDER, EMAIL_SENDER_PASSOWRD)
                        server.sendmail(EMAIL_SENDER,RECIVER_EMAIL, MESSAGE)

                    '''

                    login(request,user)
                    return redirect('index')

    return render(request,'registration/signup.html',{'form' : userdetailForm()})

@login_required
def cart(request):

    return render(request,"cart.html",{'data':"Oops Your Cart is empty!"})


@login_required
def profile(request,username):
    #purches history
    a=userShippingDetail.objects.filter(userID__username=username).values('product','purchasedDate')[::-1]
    product=[]

    for i in a:
        l=[]
        for k,v in json.loads(i['product']).items():
            l.append(v['productName'])
        l.append(i['purchasedDate'])
        product.append(l)

    print(product)
    return render(request,"profile.html",{'data':product})

@login_required
def updateprofile(request,username):
    form=updateProfileForm()

    if request.method=="POST":
        form=updateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            firstname=form.cleaned_data['firstname']
            lastname=form.cleaned_data['lastname']
            email=form.cleaned_data['email']
            pincode=form.cleaned_data['pincode']
            address=form.cleaned_data['address']
            officeaddress=form.cleaned_data['officeAddress']
            Mobile=form.cleaned_data['mobile']
            alternatemobile=form.cleaned_data['alternateMobile']
            #image
            image=form.cleaned_data['profilePhoto']
            print(Mobile,firstname,lastname,email,pincode,address,officeaddress,alternatemobile)
            data=userDetails.objects.get(user__username=username)
            if image:
                data.ProfilePicture=image
                data.save()
                print(data)


            if not  pincode ==None:
                data.pinCode=pincode
            if not  address ==None:
                data.address=address
            if not  officeaddress ==None:
                data.officeAddress=officeaddress
            if not  Mobile ==None:
                data.mobile=Mobile
            if not  alternatemobile ==None:
                data.alternateMobile=alternatemobile

            data.save()
            print(data)

            location='/profile/'+username
            return  redirect(location)

    form=updateProfileForm()

    return render(request,"updateprofile.html",{'form':form})

@login_required
def shipping(request,username):

    form=userShippingForm()
    if request.method=="POST":
        form=userShippingForm(request.POST)
        product=request.POST.get('product')
        if form.is_valid():
            name=form.cleaned_data.get('name')
            email=form.cleaned_data.get('email')
            city=form.cleaned_data.get('city')
            country=form.cleaned_data.get('country')
            pincode=form.cleaned_data.get('pincode')
            address=form.cleaned_data.get('address')
            mobile=form.cleaned_data.get('mobile')

            productJson=product
            if True:

                #############################################################
                client = razorpay.Client(auth=("rzp_test_N9RYbJpvhn8z8Q", "B1zuecce4EX1umdUZHYO0xZl"))

                total_price=0
                for _,v in json.loads(productJson).items():
                            total_price+=int(v['productPrice'])*int(v['productCount'])

                request.session['total_price']=total_price

                order_amount = total_price*100  #razors pay take subunit of price
                order_currency = 'INR'
                order_receipt = 'order_recpit_'+str((random.randint(100,10000000000000)))
                notes = {'Shipping address': address}   # OPTIONAL
                clientOrderId=client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes))
                print(clientOrderId)
                ############################################################
                newOrderId=orderStatus(orderId=clientOrderId['id'],razorpay_id="-",paymentStatus=False)
                newOrderId.save()

                data=userShippingDetail(userID=User.objects.get(username=username) ,orderId=newOrderId,name=name,email=email,city=city,country=country,mobile=mobile, pincode=pincode,address=address,product=productJson)
                data.save()


                request.session['orderId']=clientOrderId['id']
                request.session['name']=name
                request.session['email']=email
                request.session['address']=address
                request.session['pincode']=pincode
                request.session['city']=city

                return redirect('checkout')
            else:
                pass


    return render(request,"shipping.html",{'form':form})

@login_required
def checkout(request):

    orderNumber=request.session['orderId']
    data=userShippingDetail.objects.filter(orderId__orderId=orderNumber).values()

    products=json.loads(data[0]['product']) #json string to dict converter
    return render(request,"checkout.html",{"data":data[0],"product":products})

@login_required
def paymentSuccess(request):
    if request.method=="POST":
        if request.body:
            success=json.loads(request.body)
            client = razorpay.Client(auth=("rzp_test_N9RYbJpvhn8z8Q", "B1zuecce4EX1umdUZHYO0xZl"))
            try:
                client.utility.verify_payment_signature(success)
                query=orderStatus.objects.get(orderId=success['razorpay_order_id'])
                query.razorpay_id=success['razorpay_payment_id']
                query.paymentStatus=True
                query.save()
                request.session['success']=success
                '''
                #sending mail
                RECIVER_EMAIL= request.session['email']
                MESSAGE=f"""
                    subject : Thanking your for Shoppin with us

                    hey, {request.session['name']} ,Thanking you so much to shopping with us.

                    Your order ID:          {request.session['orderId']}
                    Your Razor pay ID :     {success['razorpay_payment_id']}
                    Your Total Billing :    {request.session['total_price']}

                    your address:           {request.session['address']}
                    Your Pincde :           {request.session['pincode']}
                    Your City:              {request.session['city']}

                    for more enquiry contact me : 7869319541
                    email : pawankushwah840@gmail.com

                    """

                context = ssl.create_default_context()
                with smtplib.SMTP(HOST_SERVER, HOST_PORT) as server:
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(EMAIL_SENDER, EMAIL_SENDER_PASSOWRD)
                    server.sendmail(EMAIL_SENDER,RECIVER_EMAIL, MESSAGE)
                '''
                return HttpResponse('PaymentSuccess')


            except:
                pass

    return redirect('/paymentFailer/')

@login_required
def paymentFailer(request):
    return redirect('/paymentFailer/')

def trackorder(request):

    if request.method=="GET" and request.GET.get('search',False):
        oId=request.GET.get('search',"-")
        a=trackOrder.objects.filter(orderId__orderId=oId).values()
        if len(a):
            return render(request,"track.html",{'dataFound':a[0]})
        else:
            return render(request,"track.html",{'NodataFound':"No data Found, Please Write Order Id carefully"})
    else:
        return render(request,"track.html")
