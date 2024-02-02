#a view to handle the form and create a new Order
from django.shortcuts import render,redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from .models import Order
from  .tasks import order_created
from django.urls  import reverse
from django.shortcuts import render, redirect

    


def order_create(request):
    # Creating an instance of class Cart and passing a request to it
    cart = Cart(request)
    
    # Checking if the HTTP request method is equal to POST
    if request.method == 'POST':
        # Creating an instance of OrderCreateForm, then populating it with data submitted by the user
        # and assigning this instance to a variable 'form' for further processing/validation in view function
        form = OrderCreateForm(request.POST)
        
        # An if statement that checks if the form is valid
        if form.is_valid():
            # Creating an object that stores details of the form
            order = form.save()
            
            # Looping items from the cart
            for item in cart:
                # This is a method call on the objects manager of the OrderItem model in Django.
                # It provides methods for querying the database. 'create' is a method used to create a new object in the database.
                OrderItem.objects.create(
                    order=order, 
                    product=item['product'], 
                    price=item['price'], 
                    quantity=item['quantity']
                )
                
            # Clearing objects from the cart
            cart.clear()
            
            order_created.delay(order.id)
            
            # Rendering the template after passing 'order' to the template context
            return render(request, 'orders/order/created.html', {'order': order})
    
    else:
        # Creating an instance of OrderCreateForm class
        # Used to render an HTML form in a Django template or to process form data submitted by a user in a view function
        form = OrderCreateForm()
        
    # Rendering the 'create.html' template after passing 'cart' and 'form' to the template context
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})






        
        
    
                   





