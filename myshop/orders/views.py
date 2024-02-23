#a view to handle the form and create a new Order
from django.shortcuts import render,redirect, get_object_or_404
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from .models import Order
from  .tasks import order_created
from django.urls  import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem,Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import  weasyprint








    


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



@staff_member_required        
#checks that both the is_active and  is_staff fields of user requesting the page are set to True
def admin_order_detail(request, order_id):
    order  =  get_object_or_404(Order, id=order_id)
    #getting Order object with given ID and rendering a template to display Order
    return render(request, 'admin/orders/order/detail.html', {'order':order})
  





@staff_member_required
#decorator that  makes  sure  only staff users can acess this view
def admin_order_pdf(request,order_id):
    
    order  = get_object_or_404(Order, id=order_id)
    #getting the order id 
    html  = render_to_string('orders/order/pdf.html', {'order':order})
    #rendering the order/order
    
    
    response  = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    #used to genearate a pdffile  from rendered HTML code and write to HttpResponse object
    
    return  response

#a view  to generate  a pdf   invoice  for an order
    
    
        
        
    
                   





