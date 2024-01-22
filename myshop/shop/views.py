from django.shortcuts import render,get_object_or_404
from .models import Category,Product
from cart.forms  import CartAddProductForm




#View for retrieving available products
def product_list(request, category_slug=None):
    #This  function takes request as a parameter and category_slug=None as an optional parameter
   
    categories  = Category.objects.all()
    # this line of code that fetches  all categories from category model in database
    #and stores them in  variable categories
    products  = Product.objects.filter(available=True)
    #Retrieves all  Product object  from database where the available field is set to True
    
    if category_slug:
        #checks if the category is provided in the URL
        category = get_object_or_404(Category, slug=category_slug)
        #if a category-slug is provided , it retreives the Category object
        #with the matching slug from database,if not found returns a 404  error page
        products = products.filter(category=category)
        #filters products based on specified category and narrow down  the list of products 
        # to only those that belong to the selected category
        
    return render(request, 'shop/product/list.html', {'categories': categories, 'products': products})   
    # Renders the  shop/product/list.html template with a dictionary of context data
    
    
    
#view for retrieving a single product

def product_detail(request, id, slug):
    #passing request,id and slug as parameteres
    product = get_object_or_404(Product, id=id,slug=slug,available=True)
    #retrieves a single  object instance of the Product model from the database and 
    #stores it to variable product and if not found raises a 404 HTTP response
    
    cart_product_form = CartAddProductForm()
    #instance of class cart_product_form  that handles user inputs and validations
    
    return render(request,'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form})
#The product_detail view  expects the id and slug  parameters in order to retrieve the Product instance

 
    
    
    