from email.policy import default
from django.db import models
from django.db.models import Model
import os
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator
# Create your models here.

#Doctors
class Doctors(models.Model):
    name = models.CharField(max_length=100, unique=True)
    position = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    picture = models.ImageField(max_length=100, upload_to='images')

#Medicine Supplies
class Medicine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dosage = models.CharField(max_length=100)
    medicine_type = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    picture = models.ImageField(max_length=100, upload_to='medicine')


# Patients/User Accounts
class Registration(AbstractUser):
    user_type = [
        ('P', 'Patient'),
        ('A', 'Administration'),
    ]
    
    birthday = models.DateField(null=True)
    phoneNumberRegex = RegexValidator(regex = r"^(09|\+639)\d{9}$")
    c_number = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True)
    # c_number = models.IntegerField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=30)
    user_type = models.CharField(max_length=30, choices= user_type, verbose_name='user_type', default ='A')


#Appointment
class Appointment(models.Model):
    patient = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reasons = models.CharField(max_length=500)



#News and Update
class News_and_Updates(models.Model):
    news_and_updates = models.ImageField(max_length=100, upload_to='news_and_updates')
    headline = models.CharField(max_length=200)
    fb_link = models.CharField(max_length=200)


#Staff
class Staff(models.Model):
    staff_picture = models.ImageField(max_length=100, upload_to='staff')
    year = models.CharField(max_length=200)