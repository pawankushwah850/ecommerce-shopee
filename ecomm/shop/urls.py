from django.urls import path,include
from . import views
from django.views.generic import TemplateView

urlpatterns=[
    #front page,menu
    path('',views.index,name="index"),
    #views product by category
    path('category/<args>/',views.category,name="cat"),
    path('signup/',views.signup,name='signup'),
    path('profile/<str:username>',views.profile,name="profile"),
    path('updateprofile/<str:username>',views.updateprofile,name="updateprofile"),


    path('cart/',views.cart,name="cart"),
    path('shipping/<str:username>',views.shipping,name="shipping"),

    path('term&condition/',TemplateView.as_view(template_name="termCondition.html")),
    path('policy/',TemplateView.as_view(template_name="policy.html")),

    path('checkout/',views.checkout,name="checkout"),

    path('paymentSuccess/',views.paymentSuccess,name="paymentSuccess"),
    path('success/',TemplateView.as_view(template_name="payment/success.html")),

    path('paymentFailer/',views.paymentFailer,name="paymentFailer"),


    path('trackorder/',views.trackorder,name="trackorder"),

    ]