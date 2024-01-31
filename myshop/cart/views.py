from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm



#This is the view  for adding products to the cart or updating the quantities for existing products
@require_POST
#@require_POST decorator to allow  only POST requests
def cart_add(request, product_id):
    #passing product_id as a parameter
    cart = Cart(request)
    #creating an instance of class Cart and passing  the request object
    product = get_object_or_404(Product, id=product_id)
    #getting  product object from database using the provided product_id
    form = CartAddProductForm(request.POST)
    #creating  an instance of  the CartAddProductForm class and pass the POST data to it
    if form.is_valid():
        #if the form is valid, get cleaned data from  the form
        cd  = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
        #Calls the add method on the cart object to add specified product with specified
        #quantity to the shopping cart
        return redirect('cart:cart_detail')
    #Redirects the user to the cart detail page after successfully adding the product to the cart
    
    
    
    return render(request, 'cart_detail.html',{'form':form})
#a view to remove items from the cart

@require_POST
#require_POST decorator to allow only POST requests
def cart_remove(request, product_id):
    #passing product_id as a paramter
    cart = Cart(request)
#creating an instance of class  Cart and passing a request
    product  = get_object_or_404(Product, id=product_id)
#retrieving the Product instance with product_id
    cart.remove(product)
    #removing the existence of the product
    return  redirect('cart:cart_detail')
    #redirecting the user to the  cart_detail URL
    
    
    
    
    
    
    
    
#a view to   get  the current cart and display it~
def   cart_detail(request):
    #passing request as a parameter
    cart = Cart(request)
    #creating an instance of class Cart and passing a request
    return  render(request, 'cart/detail.html',{'cart':cart}) 



# 
def  product_detail(request, id,slug):
    #passing request,id, slug as a parameter
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    #Getting the product based on the provided id and slug, if not found,return a 404 page
    cart_product_form = CartAddProductForm()
    #creating an instance  of the CartAddProductForm,this form is typically used to handle adding
    #products  to a shopping cart
    
    return render(request,'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form})
    # Render the detail.html template with the product information and cart form as context variables
    

    

#This views gets the current cart and displays it
def cart_detail(request):
    #passing request as a parameter
    cart = Cart(request)
    #creating instance of class cart and  passing a request
    
    for item in cart:
        #This is a loop that iterates over each item in the cart possible a list of items 
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item['quantity'],'override':True})
    
    return render(request, 'cart/detail.html',{'cart':cart})
"""


created  an instance of CartAddProductForm for each  item in  the cart to allow  changing product
quantities .I initialize the form with the current item quantity and set the override field to True
so that when I submit the form to the cart_add view,current quantity is replaced with new one



"""




  
      