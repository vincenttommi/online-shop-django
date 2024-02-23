from django.urls import path
from  .  import views



app_name   = 'coupons'



urlpatterns = [
    
    path('apply/', views.coupon_apply, name='apply'),
    #registering view of the coupon view in  apps url
    
]
