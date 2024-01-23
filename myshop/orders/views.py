#a view to handle the form and create a new Order
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart





def order_create(request):
    #function order_create receiving request as a parameter
    cart = Cart(request)
    #creating an instance of class cart and passing a request to it
    if request.method  == 'POST':
        #This line checks if the HTTP  request method is POST
        form = OrderCreateForm(request.POST)
        #if the requested method is POST a form instance is created using OrderCreateForm from
        #class OrderCreateForm
        
        if form.is_valid():
            #after creating the  instance the  the form checks if the data is valid  before executing the code
            order  =  form.save()
            #if the form is valid the  the data is being saved to a new object created called  order
            for item in cart:
                #iterating items in cart  by looping them individually
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],quantity=item['quantity'])
                #This line of code is creating a new  order item  object in database with specific 
                # values  for it's field
    
        # clear the cart
        cart.clear()
        
        return render(request, 'orders/order/created.html',{'order':order})
    #renders the orders/order/created.html
    else:
        form  = OrderCreateForm()
        #a new instance of OrderCreateForm is being created
        return render(request, 'orders/order/create.html',{'cart':cart,'form':form })
        