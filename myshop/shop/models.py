from django.db import models


#Category model
class Category(models.Model):
    
    name = models.CharField(max_length=200)
    slug =  models.SlugField(max_length=200, unique=True)
    
    
    class Meta:
        ordering  = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        
        verbose_name = 'category'
        verbose_name_plural  = 'categories'
        
        
        def __str__(self):
            return  self.name
        
        
        
        
#Product model 
class Product(models.Model):
    category =models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    #A Foreignkey to the Category model.This is a one to many relationship
    #a product belongs to  one category and category contains multiple products
    name  = models.CharField(max_length=200)
    #name of the product 
    slug = models.SlugField(max_length=200)
    #Slug for  product to build beautiful URLs
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    #field for capturing optional product image
    
    description = models.TextField(blank=True)
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    #The field uses  python decimal.Decimal type to  store a fixed-precision decimal number
    available =  models.BooleanField(default=True)
    #Boolean value used to indicate wether product is  available or not
    # used to enable/disable the product in the catalog
    created = models.DateTimeField(auto_now_add=True)
    #stores when the product was created
    updated  =  models.DateTimeField(auto_now=True)
    #Store when the object was last updated 
    
    
    class Meta:
        ordering  = ['name']
        indexes  = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        
    def __str__(self):
        return self.name    