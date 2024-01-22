from  .cart import Cart

#creating a context processor to set the current cart into request context

def cart(request):
    return{'cart':Cart(request)}
"""

In the context processor , I instantiate the cart using the request object and make i
available for templates as a variable named cart

"""


