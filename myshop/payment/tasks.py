from io import BytesIO
#python module that provides support for handling  I/O input/output operations 
from  celery import shared_task
import  weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models  import Order 



@shared_task
def payment_completed(order_id):   
    """
    
    Task to send an e-mail notification when an  order is  successfully paid
    
    """
    
    order  = Order.objects.get(id=order_id)
    #an instance of order class that gets the id from Column Order from database
    subject  =  f'My shop  - Invoic no . {order.id}'
    message =  'please, find attached  the invoice  for  your recent  purchase'
    email =  EmailMessage(subject,message, 'admin@myshop.com', [order.email])
    
    
    
    #generating PDF
    html  = render_to_string('orders/order/pdf.html', {'order':order})
    out  = BytesIO
    #creating an instance of BytesIO and assigning it to out variable
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT /  'css/pdf.css')]
    #function provided by WeasyPrint library  to create a CSS object.
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    #Takes html input as a string 
    



    #attaching PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    
    
    #sending e-mail 
    email.send()
    