from django.db import models


# Create your models here.
# class Visitorsmessage(models.Model):
#     #image = models.ImageField(upload_to='portfolio_images/', blank=True)
#     name = models.CharField(max_length=25)
#     email= models.EmailField(max_length=30)
#     phone_number = models.IntegerField()
#     gender= models.CharField(max_length=18)
#     #age=models.IntegerField()
#     subject = models.CharField(max_length=200)
#     message = models.TextField()
#
#     def __str__(self):
#         return self.name

from django.db import models

class Visitorsmessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"


