from django.db import models

# Create your models here.
class MainCategory(models.Model):
    maincategory_id=models.CharField(primary_key=True,max_length=100)
    maincategory_name= models.CharField(max_length=100)

    def __str__(self):
        return self.maincategory_name


    def generate_maincategory_id(self):
        pattern = "EZMC"
        maincategory_pattern = MainCategory.objects.filter(maincategory_id__startswith=str(pattern))
        count = maincategory_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.maincategory_id:
            self.maincategory_id = self.generate_maincategory_id()

        super().save(*args, **kwargs)


    class Meta:
        db_table = "maincategory_table"

class SubCategory(models.Model):
    subcategory_id=models.CharField(primary_key=True,max_length=100)
    subcategory_name=models.CharField(max_length=100)
    maincategory_id=models.ForeignKey(MainCategory,related_name='main',on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name

    def generate_subcategory_id(self):
        pattern = "EZSC"
        subcategory_pattern = SubCategory.objects.filter(subcategory_id__startswith=str(pattern))
        count = subcategory_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.subcategory_id:
            self.subcategory_id = self.generate_subcategory_id()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "subcategory_table"

class Event(models.Model):
    event_id = models.CharField(primary_key=True,max_length=100)
    event=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()

    def _str_(self):
        return self.event

    def generate_event_id(self):
        pattern = "EZE"
        event_pattern = Event.objects.filter(event_id__startswith=str(pattern))
        count = event_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.event_id:
            self.event_id = self.generate_event_id()

        super().save(*args, **kwargs)
    class Meta:
        db_table = "event_table"
