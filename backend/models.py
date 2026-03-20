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