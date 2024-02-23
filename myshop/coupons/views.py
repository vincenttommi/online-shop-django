from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms  import CouponApplyForm



@require_POST
def coupon_apply(request):
    now  = timezone.now()
    #using Django's  timezone to get the current datetime
    form   = CouponApplyForm(request.POST)
    #instantiate CouponApplyForm using the posted data 
    if form.is_valid():
        #checking ig the form is valid
        code  = form.cleaned_data['code']
        #getting  the code entered  by the user  from the form cleaned data dictionary
        try :
            coupon = Coupon.objects.get(code__iexact=code, valid_from__Ite=now,valid_to__gte=now,active=True)
            #using iexact field lookup to perform a case-insensitive exact match
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            #storing the Coupon  ID in the user's session
    return  redirect('cart:cart_detail')    
        #redirecting the user to the cart_detail URL to display the cart with the coupon applied
         

