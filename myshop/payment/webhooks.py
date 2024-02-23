import  stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks  import payment_completed





@csrf_exempt
#decorator used to prevent Django from performing the CSRF  validation that is done by default
#for all POST requests
def stripe_webhook(request):
    #receives request as a paramter
    payload = request.body
    #Extracts  the raw requestbody  from the HTTP request
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    #extracts  the value of the stripe-Signature  header from the request META attribute
    event = None
    #initailizing event variable to none
    try:
        """
        Attempts to construct a stripe event object using the construct_event method
        """
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET)
        
    except  ValueError as e:
        #Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        #invalid  signature
        return  HttpResponse(status=400)
    #if the payload is invalid or the signature verification fails , returns HTTP
    #response with a status code of 400 Bad request
    return  HttpResponse(status=200)
    #if the event is successfully constructed and verified  this line returns 
    #an  HTTP response of 200
    
    if event.type == 'checkout.session.completed':
        #is a comparison operator that checks if the  value  of event.type is equal to string
        session = event.data.object
        #assigns value of  object attribute from data attribute of event object to a variable session
        if session.mode  == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            #marking order as paid
            order.paid = True
            order.save()
            
            
            #launch asynchronous task
            payment_completed.delay(order.id)
            
          
          
        return  HttpResponse(status=200)    
    #payment_completed  task is queued by  calling  it's delay method
    #The task will be added  to the queue and will be excecuted  by a Celery worker
    #as soon as possible
            
            

"""

we check if the  event received is checkout.session.completed
This event indicates  that the checkout session has been successfully completed and we retrieve event
object and check wether the session mode is payment because is expected  mode of one-off payments
"""
            
             
        
                

    
    
    
    
#Thid function handles incoming webhooks from stripe 