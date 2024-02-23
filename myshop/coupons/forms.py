from django import forms
#form that the user will use to enter coupon code




class  CouponApplyForm(forms.Form):
    code =  forms.CharField()
    