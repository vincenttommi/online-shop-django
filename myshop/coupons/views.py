from django.utils import timezone
from django.shortcuts import redirect,render
from .forms import CouponApplyForm
from .models import Coupon
from django.views.decorators.http import require_POST
from django.contrib import messages

@require_POST
# def coupon_apply(request):
#     # Get the current time
#     now = timezone.now()
#     print("now",now)
#     # Instantiate CouponApplyForm using the posted data
#     form = CouponApplyForm(request.POST)
    
#     # Checking if the form is valid
#     if form.is_valid():
#         # Getting the code entered by the user from the form cleaned data dictionary
#         code = form.cleaned_data['code']
#         print("code",code)
        
#         try:
#             # Querying the Coupon object with specified conditions
#             coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
#             print("Coupon found:", coupon)  # Debug statem
#             # Storing the Coupon ID in user's session
#             request.session['coupon_id'] = coupon.id
#         except Coupon.DoesNotExist:
#             # If the coupon does not exist, set the coupon ID in the session to None
#             request.session['coupon_id'] = None
            
#             print("Coupon does not exist or is inactive.")
        
#         # Redirect the user to the cart detail page to display the cart with coupon applied
#         return redirect('cart:cart_detail')

def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                         valid_from__lte=now,
                                         valid_to__gte=now,
                                         active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, 'Coupon applied successfully!')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'Coupon does not exist or is inactive.')
    return redirect('cart:cart_detail')