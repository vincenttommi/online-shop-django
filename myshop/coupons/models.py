from django.db import  models
from django.core.validators import MinValueValidator, MaxValueValidator
#callable  that takes a value and raises a validationError if it doesn't meet certain criteria







class Coupon(models.Model):
    
    code  = models.CharField(max_length=50, unique=True)
    #field that stores codes that users have to enter in order to apply coupon 
    valid_from  = models.DateTimeField()
    #The datetime value that indicates when the coupon becomes valid
    valid_to  = models.DateTimeField()
    #The datetime  value that indicates when the coupon  becomes valid
    discount  =  models.IntegerField(
        validators = [MinValueValidator(0), MaxValueValidator(100)],help_text = 'Percentage value ( 0 to 100)' )
    #The field that stores the discount rate to appl
    
    active  = models.BooleanField()
    #A Boolean that indicates whether the coupon is active
    
    
    def __str__(self):
        return self.code

#models used  to store  coupons 