# Import necessary modules
from decimal import Decimal
from django.conf import settings
from shop.models import Product

# This is the Cart class that will allow me to manage the shopping cart.
# The cart is initialized with a request object
class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        # storing the current session self.session = request.session to
        # make it accessible to the other methods of the Cart class
        cart = self.session.get(settings.CART_SESSION_ID)
        # try to get the cart from the current session with the above query
        # if no cart is present in the session, I create an empty cart by setting an empty
        # dictionary in session
        if not cart:
            # Initialize an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Method to add products to the cart or update their quantity (add and save methods)

    # Function for adding products to the cart
    def add(self, product, quantity=1, override_quantity=False):
        """
        Adding a product to the cart or updating its quantity
        """
        # converting the product_id from a decimal to String for serialization
        product_id = str(product.id)
        # Check if the product is not already in the cart
        if product_id not in self.cart:
            # if not add the product to the cart with initial quantity and price
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        # Check if override_quantity is True
        if override_quantity:
            # if True, set the quantity to specified quantity
            self.cart[product_id]['quantity'] = quantity
        else:
            # if False, increment the quantity by the specified quantity
            self.cart[product_id]['quantity'] += quantity
            self.save()
            # save the changes

    # Method for removing products from the cart
    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        # converting product id from decimal to string
        if product_id in self.cart:
            # checking if product_id exists in self.cart
            del self.cart[product_id]
            # if the product is found in the cart, it is removed from the cart by using the
            # del statement on the corresponding key in the cart
            self.save()
        # saving the method after deleting items

    # Defines an iterator for a class, allowing it to iterate over items in a shopping cart
    # it retrieves product objects from the database based on product IDs in the cart,
    # updates the cart with these product objects, performs some type conversions,
    # and yields the updated cart
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database
        """
        product_ids = self.cart.keys()
        # getting the products objects and adding them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Method to return the total number of items in the cart
    def __len__(self):
        """
        Counting all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
        # returning the sum of quantities all in the cart items

    # Method to calculate the total cost of items in the cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # Method for clearing cart session
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
