from django  import forms
from .models import Order



class OrderCreateForm(forms.ModelForm):
    class  Meta:
        model = Order
        fields  = ['first_name', 'last_name', 'email', 'address','postal_code', 'city']
 
 
 
#a form that am going  to use to create  a new Order objects
 
        