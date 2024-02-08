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

    


def  order_create(request):
    
    cart = Cart(request)
    
    if request.method  =='POST':
        
        form = OrderCreateForm(request.POST)
        
        if  form.is_valid():
            
            order = form.save()
            
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                
                cart.clear()
                
                order_created.delay(order.id)
                #setting  the order in the session
                request.session['order_id'] = order.id
                #redirecting payment
                return  redirect(reverse('payment:process'))
            """
            
            Instead of  rendering the template orders/order/created.html when placing
            a new order ID is stored in the user session and user is redirected to the payment:
            process URL
            """
            
    else:
        form  = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})            






        
        
    
                   





