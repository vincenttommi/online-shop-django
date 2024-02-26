# Import necessary modules
from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

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
        
        #storing the  current applied coupon
        self.coupon_id  = self.session.get('coupon_id')
        #getting coupon_id session key from the current session and storing its value in 
        # the cart object

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



    def save(self):
        #mark the session as "modified" to make sure  it gets saved   
        self.session.modified = True


 
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
        #This line fetches all Product objects whose IDs are in the product_ids list.

        cart = self.cart.copy()
        #creates a new dictionary cart that has  the same key value-pairs as self.cart
        #This is often done to avoid unintended modifications to the original dictionary
        #working with a copy

        for product in products:
            cart[str(product.id)]['product'] = product
            #This part is accessing a specific entry in the cart dictionary

        for item in cart.values():
            #This line initiates a loop that iterates over values in the cart dictionaries
            item['price'] = Decimal(item['price'])
            #within each iteration , this line is converting the price  value of the item dictionary to a decimal type
            item['total_price'] = item['price'] * item['quantity']
            #a new key total_price is added to the item dictionary and its value is  calculated
            #by multplying the price  by the quantity
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
    #it calculates the  product of decimal representation of price and quantity

    # Method for clearing cart session
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()


    @property
    #defining this method as a property
    def coupon(self):
        #def coupon that recieves self as a parameter
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except  Coupon.DoesNotExist:
                  pass 
        return None    
    
        
        #if the cart contains  a coupon,I retrieve  it's discsount rate and  return the 
        #amount to be deducted
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0) 
    
    def  get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
    #returning the total amount of the  the cart after deducting the amount returned  by
    #get_discount method
    
    
    

       