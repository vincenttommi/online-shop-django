from django.shortcuts import render,get_object_or_404
from .models import Category,Product




#View for retrieving available products
def product_list(request, category_slug=None):
   
    categories  = Category.objects.all()
    products  = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {'categories': categories, 'products': products})   
    
    
    


#view for retrieving a single product


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,slug=slug,available=True)
    
    return render(request,'shop/product/detail.html',{'product':product})
#The product_detail view  expects the id and slug  parameters in order to retrieve the Product instance

 
    
    
    