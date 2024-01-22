from django.urls  import path
from .views import cart_add, cart_remove, cart_detail

# from .views import cart_view  # Import your cart view


app_name  = 'cart'    
#setting the app namespace  


urlpatterns = [
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/',cart_remove, name='cart_remove'),
    path('detail/', cart_detail, name='cart_detail'),
   
]
