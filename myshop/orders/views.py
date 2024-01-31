#a view to handle the form and create a new Order
from django.shortcuts import render,redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from .models import Order



def order_create(request):
    #taking request as a parameter
    cart = Cart(request)
    # creating instance of class Cart and passing a request
    if request.method  == 'POST':
        #checking if the Http request method is equal to POST
        form = OrderCreateForm(request.POST)
        #creating an instance of OrderCreateForm and assigning Post request
        if form.is_valid():
            #checking if the form is valid
            order = form.save()
            #creating an object order and saving  details of the form
            
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                
                
                #clear cart
                cart.clear()
        return  render(request, 'orders/order/created.html', {'order':order})  
 
    else:
        form  = OrderCreateForm()
        #creating an instance of OrderCreateForm object and assigning it to form
        return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})
    
     
                
                



# def order_create(request):
#     #passing request object as a parameter
#     if request.method  == 'POST':
#         #checking if the HTTP request method is POST
#         form  = OrderCreateForm(request.POST)
#         #creating an instance  of OrderCreateForm with POST data
#         if form.is_valid():
#             #checking if the form data is valid
#             order = form.save()
#             #saving the form data  to the database to create a new order
#             cart.clear()
#             #clearing the cart
            
#             order.created.delay(order.id)
#             #launching an asynchronous task to handle  the order creation
#             return redirect('order_sucess')
#             #redirecting to a sucess page after the order is successfully created
#     else:    
#         form = OrderCreateForm()
#         #creating an instance of  OrderCreateForm without any data(for get requests)
#         return render(request, 'create.html', {'form':form})
#         #rendering the 'order_created.html' template  with form object
            
    
        

""""


this code snippet is part of an order creation process in django web application
that handles  the form submission clears the shopping cart and  asynchronoulsy processses the order creation using Celery


"""          