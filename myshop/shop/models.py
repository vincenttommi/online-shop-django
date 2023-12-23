from django.db import  models
from django.urls import reverse


# Category Model
class  Category(models.Model):
    name  = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200,unique=True)
    #   
    
    class Meta:
        ordering  = ['name']
        indexes  = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
        
        
        def  get_absolute_url(self):
            return reverse('shop:product_list_by_category', args=[self.slug])
        
       
        
        
 #products model 
class  Product(models.Model):
    Category  = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    #A foreignkey to Category Model This is a one-to-many relationship, aproduct belongs to one category  and a category contains  muiltiple products
    name =  models.CharField(max_length=200)
    #The name of the product
    slug = models.SlugField(max_length=200)
    #The Slug for this product to build  beautiful URLS.
    image  = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    #field of an optional image
    description  = models.TextField(blank=True)
    #An optional description of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #The field uses  pythons's decimal. Decimal type to store a fixed-precision decimal number
    #The maximum number of  digits(including the decimal places) is set using the max_digits attribute and decimal_places attribute
    available  = models.BooleanField(default=True)
    #A Boolean valaue that indicates  wether the product is  available or not
    created  = models.DateTimeField(auto_now_add=True)
    #This field  stores when the obect  was created
    updated  = models.DateTimeField(auto_now=True)
    #This field stores when the  object was last updated 
    
    class  Meta:
        ordering  = ['name']
        indexes  = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
            
            
    def  get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id,self.slug])
    #Convention to retrieve the URL for a given object
    
      
       
       