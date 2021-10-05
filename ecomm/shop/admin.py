from django.contrib import admin
from shop.models import product,userDetails,userShippingDetail,orderStatus,trackOrder
# Register your models here.

class productAdmin(admin.ModelAdmin):
    list_display=('productId','productName','categoryType','productPrice','publishDate',)
    search_fields=('id','productName',)
    date_hierarchy="publishDate"
    list_filter=('publishDate',)

class userDetailsAdmin(admin.ModelAdmin):
    list_display=('user','pinCode','address','officeAddress','mobile','alternateMobile','registrationDate',)
    search_fields=('user__username','pinCode','alternateMobile')
    date_hierarchy="registrationDate"
    list_filter=('registrationDate',)

@admin.register(userShippingDetail)
class userShippingDetailAdmin(admin.ModelAdmin):
    list_display=('userID','orderId','name','email','city','country','pincode','address','mobile','purchasedDate')
    date_hierarchy='purchasedDate'
    search_fields=('userID__username','orderId__orderId','pincode','mobile','city')

@admin.register(orderStatus)
class orderStatusAdmin(admin.ModelAdmin):
    list_display=('orderId','razorpay_id','paymentStatus','date',)
    date_hierarchy='date'
    search_fields=('orderId','razorpay_id',)
    list_filter=('date',)

@admin.register(trackOrder)
class trackOrderAdmin(admin.ModelAdmin):
    list_display=('orderId','stage1','stage2','stage3','stage4','stage5','stage6','stage7','delivery','orderReceived','orderReceivedDate')
    date_hierarchy='orderReceivedDate'
    search_fields=('orderId__orderId',)
    list_filter=('orderReceivedDate',)

admin.site.register(userDetails,userDetailsAdmin)
admin.site.register(product,productAdmin)