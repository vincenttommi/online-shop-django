#Registering catalog models  on the administartion site
from django.contrib import  admin
from .models import Category,Product





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug']
    prepopulated_fields  = {'slug':('name',)}
    #used to  specify fields where the value is automatically  set using the  value  of other  fieblds
    #This convient for generating slugs
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'price','available','created','updated']    
    list_filter = ['available','created','updated']
    list_editable = ['price','available']
    #setting the fields that are editable  from the  list  display  of the administration site
    prepopulated_fields = {'slug':('name',)}
    
    