from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    Address = models.TextField(max_length=1000)
    contact = models.CharField(max_length=15)
    dob = models.DateField(verbose_name='Date of Birth',null=True,blank=True)
    
    SPECIALISATION_CHOICES = [
        ('Health Insurance','Health Insurance'),
        ('Vehicle Insurance','Vehicle Insurance'),
        ('Fire Insurance','Fire Insurance'),
        ('Travel Insurance','Travel Insurance'),
    ]

    specialisation = models.CharField(choices=SPECIALISATION_CHOICES,max_length=40)
    profile_image = models.ImageField(upload_to='Profile_images/')

    def __str__(self):
        return self.username

class Campaign(models.Model):
    title = models.CharField(max_length = 500)
    location = models.CharField(max_length = 500)
    assign_agents = models.ForeignKey(User,on_delete = models.CASCADE)
    poster = models.ImageField(upload_to='poster/')
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)  
    latitude = models.TextField(null=True,blank=True)
    longitude = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title
    
class Client(models.Model):

    QUALIFICATION_CHOICES = [
        ('sslc','SSLC'),
        ('HSE','Higher Secondary'),
        ('bachelors','Bachelors'),
        ('masters','Masters')
    ]

    full_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(max_length=1000,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    contact = models.CharField(max_length=10,null=True,blank=True)
    aadhar = models.CharField(unique=True,max_length=12,null=True,blank=True)
    pan = models.CharField(max_length=10,unique=True,null=True,blank=True)
    job = models.CharField(max_length=100,null=True,blank=True)
    salary = models.IntegerField(null=True,blank=True)
    qualification = models.CharField(choices=QUALIFICATION_CHOICES,max_length=100)
    status = models.CharField(max_length=10,null=True,blank=True)
    interest = models.TextField(max_length=5000,null=True,blank=True)
    agent_feedback = models.TextField(max_length=5000,null=True,blank=True)
    feedback = models.TextField(max_length=5000,null=True,blank=True)
    agent = models.ForeignKey(User,on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.full_name