from django import  forms
#import forms from django



PRODUCT_QUANTITY_CHOICES  = [(i, str(i)) for i in range(1, 21)]
#This line creates  a list of tuples  named 'PRODUCT_QUANTITY_CHOICES
#it's a list comprehension that generates with integers from 1 to  20 inclusive with their string
#representation




#This line  defines a  form class named CartAddProductForm that inherits from forms.Form
#used in creating a form for adding products to a shopping cart
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    #This line defines  a form field  named  quantity ,uses forms.TypedChoiceField 
    #to create a field where the user can choose a quantity from a predefined list
    #of choices
    #coerce=int  ensures that the choosen value is  converted to an integer
    
    
    override =  forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
    #This allows  to indicate  whether the quantity has to be added to any existing quantity
    #in the cart for this product(False), or wether the existing quantity has to be overridden
    #with  given quantity(True)
    
    