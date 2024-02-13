from django.db import models
from shop.models import Product
from django.conf import settings


"""



I will need a model to store  order details and model to store items bought, including their price
and quantity


"""





class Order(models.Model):
    first_name  = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code  = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    
    
    class Meta:
        ordering= ['-created']
        #defines how  instances of this model should be ordered when retrieved from database
        indexes = [
            models.Index(fields=['-created']),
            #An index is a database optimzation that makes  certain types of queries fast
        ]
        
       
    def __str__(self):
        #recieves self as a paramete
        return f'Order{self.id}'
    #This line returns a formatted string  that represents the object order followed by attribute
    #id 
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    #This line calculates the total cost by summing up  the costs of individual items  associated with
    #current instance
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    stripe_id  = models.CharField(max_length=250, blank=True)
    
 
 
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return  self.price * self.quantity 
    #get_total_cost() method  to obtain the total cost of items bought in this order
        
        
  
#This method is used to  return stripe dashboard's URL for payment associated with order 
    def  get_stripe_url(self):
        #method to get stripe url
        if not self.stripe_id:
            # no payment associated 
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            #   Stripe path for test payments
            path  = '/test/'
        else:
            #Stripe path for real  payments
            path  = '/'
             
        return f'http://dashboard.stripe.com{path}payments/{self.stripe_id}'        
    
    
    
           