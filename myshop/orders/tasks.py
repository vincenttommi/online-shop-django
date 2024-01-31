from celery import  shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
#celery decorator used to define a task and  marks function below as celery task that can be excuted asynchrously
def order_created(order_id):
    #retrieves order_id as a parameter
    """
    Task to send an e-mail notification when an order is successfully created
    """
    order = Order.objects.get(id=order_id)
    #retrieves  order object  from database  using order_id
    
    subject = f'Order nr.{order_id}'
    # creates the subject line for email
    message  = f'Dear {order.first_name},\n\n'
   
    f'You have successfully placed an order.'
    f'Your order ID is {order_id}.'
     #initailise email message
    
    
    mail_sent = send_mail(subject, message,'admin@myshop.com',)
    #this line sends the email using django
    
    
    return  mail_sent
    
    
#This function is responsible for sending an email notification when an  order is successfully created
