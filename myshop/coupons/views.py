from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def coupon_apply(request):
    # Get the current time using Django's timezone
    now = timezone.now()
    
    # Instantiate CouponApplyForm using the posted data 
    form = CouponApplyForm(request.POST)
    
    # Check if the form is valid
    if form.is_valid():
        # Get the code entered by the user from the form cleaned data dictionary
        code = form.cleaned_data['code']
        
        # Try to retrieve the coupon from the database
        try:
            # Use case-insensitive exact match for the code and check validity period
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            # Store the Coupon ID in the user's session
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            # If the coupon does not exist, set the coupon ID in the session to None
            request.session['coupon_id'] = None
    
    # Redirect the user to the cart detail page to display the cart with the coupon applied
    return redirect('cart:cart_detail')
