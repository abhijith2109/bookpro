from django.db import models

# Create your models here.

class Books(models.Model):
    book_name=models.CharField(max_length=120,unique=True)
    author=models.CharField(max_length=120)
    amount=models.PositiveIntegerField()
    copies=models.PositiveIntegerField()
    image=models.ImageField(upload_to="images",null=True)

    def __str__(self): #to string method -for print values
        return self.book_name




 # 1st Step ::>>python manage.py makemigrations -if we attempt any changes in models then we should use make migratin command
# onlt then it will generate a query file


#2nd Step ::>>python manage.py migrate changes added to database


#ORM Query >> Object Relation Mapper
#ref_name=model_name(propertytype=value,propertytype=value...)
# ref_name.save()

#fetching all records
#ref_name=modelnam.objects.all()
#`books=Books.objects.all()



