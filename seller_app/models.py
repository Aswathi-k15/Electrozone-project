from django.db import models
from admin_app.models import *


# Create your models here.
class Seller(models.Model):
    seller_id=models.CharField(max_length=100,primary_key=True)
    seller_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    license_number=models.IntegerField()
    create_date = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=100,default="pending")

    def __str__(self):
        return self.seller_name


    def generate_seller_id(self):
        pattern = "EZS"
        sellers_pattern = Seller.objects.filter(seller_id__startswith=str(pattern))
        count = sellers_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.seller_id:
            self.seller_id = self.generate_seller_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "seller_table"

class Product(models.Model):
    product_id=models.CharField(max_length=100,primary_key=True)
    product_name=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)
    price=models.IntegerField()
    seller_id=models.ForeignKey(Seller,on_delete=models.CASCADE)
    subcategory_id=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now=True,null=True)

    def __str__(self):
        return self.product_name




    def generate_product_id(self):
        pattern = "EZPDT"
        product_pattern = Product.objects.filter(product_id__startswith=str(pattern))
        count = product_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = self.generate_product_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table="product_table"

class Image(models.Model):
    image_id=models.CharField(max_length=100,primary_key=True)
    image=models.ImageField(upload_to='images/')
    product_id=models.ForeignKey(Product,related_name='images' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.image_id


    def generate_image_id(self):
        pattern = "EZIMG"
        image_pattern = Image.objects.filter(image_id__startswith=str(pattern))
        count = image_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.image_id:
            self.image_id = self.generate_image_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table="image_table"

class Mobile(models.Model):
    mobile_id=models.CharField(max_length=100,primary_key=True)
    color=models.CharField(max_length=100)
    storage=models.CharField(max_length=100)
    quantity=models.IntegerField()
    battery=models.CharField(max_length=100)
    warranty=models.CharField(max_length=100)
    price=models.IntegerField()
    product_id=models.ForeignKey(Product,related_name='mobiles',on_delete=models.CASCADE)

    def __str__(self):
        return self.mobile_id


    def generate_mobile_id(self):
        pattern = "EZM"
        mobile_pattern = Mobile.objects.filter(mobile_id__startswith=str(pattern))
        count = mobile_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.mobile_id:
            self.mobile_id = self.generate_mobile_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table="mobile_table"

class Laptop(models.Model):
    laptop_id=models.CharField(max_length=100,primary_key=True)
    color=models.CharField(max_length=100)
    storage=models.CharField(max_length=100)
    quantity=models.IntegerField()
    battery=models.CharField(max_length=100)
    warranty=models.CharField(max_length=100)
    price=models.IntegerField()
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.laptop_id


    def generate_laptop_id(self):
        pattern = "EZL"
        laptop_pattern = Laptop.objects.filter(laptop_id__startswith=str(pattern))
        count = laptop_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.laptop_id:
            self.laptop_id = self.generate_laptop_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table="laptop_table"

class Tv(models.Model):
    tv_id=models.CharField(max_length=100,primary_key=True)
    size=models.CharField(max_length=100)
    sound_output=models.CharField(max_length=100)
    quantity=models.IntegerField()
    warranty=models.CharField(max_length=100)
    price=models.IntegerField()
    product_id=models.ForeignKey(Product,related_name='tv',on_delete=models.CASCADE)

    def __str__(self):
        return self.tv_id


    def generate_tv_id(self):
        pattern = "EZT"
        tv_pattern = Tv.objects.filter(tv_id__startswith=str(pattern))
        count = tv_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.tv_id:
            self.tv_id = self.generate_tv_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table="tv_table"

class Headphone(models.Model):
    headphone_id=models.CharField(max_length=100,primary_key=True)
    color=models.CharField(max_length=100)
    sound_output=models.CharField(max_length=100 )
    quantity=models.IntegerField()
    battery=models.CharField(max_length=100)
    warranty=models.CharField(max_length=100)
    price=models.IntegerField()
    product_id=models.ForeignKey(Product,related_name='headphone',on_delete=models.CASCADE)

    def __str__(self):
        return self.headphone_id


    def generate_headphone_id(self):
        pattern = "EZHP"
        headphone_pattern = Headphone.objects.filter(headphone_id__startswith=str(pattern))
        count = headphone_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.headphone_id:
            self.headphone_id = self.generate_headphone_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table="headphone_table"

class Offer(models.Model):
    offer_id=models.CharField(max_length=100,primary_key=True)
    discount=models.IntegerField()
    event_id=models.ForeignKey(Event, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,related_name='offer', on_delete=models.CASCADE)

    def _str_(self):
        return self.offer_id

    def generate_offer_id(self):
        pattern = "EZO"
        offer_pattern = Offer.objects.filter(offer_id__startswith=str(pattern))
        count = offer_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.offer_id:
            self.offer_id = self.generate_offer_id()

        super().save(*args, **kwargs)
    class Meta:
        db_table = "offer_table"