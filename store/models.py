from django.db import models

from django.contrib.auth.models import User

class Customer(models.Model):
    # user can have 1 customer, 1 customer can have 1 user
    
    user=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="customer")

    name=models.CharField(max_length=50, null=True)
    email=models.CharField(max_length=200)

    # method to return the string value
    def __str__(self):
        return self.name #this will show on our admin panel

class Product(models.Model):
    name = models.CharField(max_length=50)
    price= models.DecimalField(max_digits=7, decimal_places=2)
    digital=models.BooleanField(default=False,null=True,blank=False)
    #boolean bc we want to know if the item is digital or not
    #if false then we have to ship it
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    #relation many to one
    #customer can many multiple orders
    #if a customer gets deleted we dont want to delete the order but null instead
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    #the status of our order
    complete = models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id) #return an id bc its a specific order

    @property
    def shipping(self):
        shipping= False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

#see how many items are in our cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    #a single order can have multiple order items
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity= models.IntegerField(default=0, null=True, blank=True) #increment as we add an item
    date_added=models.DateTimeField(auto_now_add=True)#the date we added this item to our order

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

class ShippingAddress(models.Model):
    #we want to attach it to a customer bc if an order gets deleted we still want a shipping address for the customer
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address= models.CharField(max_length=100, null=False)
    city= models.CharField(max_length=100, null=True)
    state=models.CharField(max_length=100, null=False)
    zipcode= models.CharField(max_length=100, null=False)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address