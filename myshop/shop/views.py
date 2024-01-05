from django.shortcuts import render, get_list_or_404
from  .models import Category,Product






def product_list(request,categor_slug=None):
    category  = None
    categories  = Category.objects.all()
    products = Product.objects.filter(available=True)
    #filtering the available=True to retrieve only available products
    if categor_slug:
        category = get_list_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {'category':category, 'categories':categories,'products':products})
    
#a view to retrieve and display  a singel product

def product_detail(request, id,slug):
    
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    
    
    return render(request, 'shop/product/detail.html',{'product':product})

#product_detail view expects the id and  slug parameteres in order to retrieve Product instance



 