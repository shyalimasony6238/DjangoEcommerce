from django.db import models

# Create your models here.
class pro_category(models.Model):
    pro_name=models.CharField(max_length=50)
    pro_description=models.CharField(max_length=200)
    pro_cat_image=models.ImageField(upload_to="category_image")

    def __str__(self):
        return self.pro_name

  
class protable(models.Model):
    category = models.ForeignKey(pro_category, on_delete=models.CASCADE)
    pro_name=models.CharField(max_length=50)
    qty=models.IntegerField()
    price = models.IntegerField()
    p_image=models.ImageField(upload_to="product_image")

from django.contrib.auth.models import User
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(protable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):   # ✅ INSIDE class
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.pro_name}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username    
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name