from django.contrib.auth.models import User
from django.db import models
# from django.
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=128,null=True,blank=True)
    email=models.EmailField(max_length=128,null=True,blank=True,unique=True)
    dob=models.DateField(null=True,blank=True)
    contactnumber=models.CharField(max_length=20,null=True,blank=True,unique=True)
    address=models.TextField(null=True,blank=True)
    gender=models.IntegerField(null=True,blank=True,default=None)
    profile_picture=models.FileField(upload_to="user_profile",null=True,blank=True)
    lastlogin=models.DateTimeField(null=True,blank=True)


