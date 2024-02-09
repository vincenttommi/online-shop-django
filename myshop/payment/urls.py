from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    
    path('process/',views.payment_process, name='process'),
    #registering a view that displays  order summary to the user, creates the stripe
    #checkout session and redirects  the user to Stripe-hosted payment form
    path('completed/', views.payment_completed, name='completed'),
    path('cancelled/', views.payment_cancelled, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
    #registering webhook  view in urls 
    
]
