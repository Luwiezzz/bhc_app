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
    picture = models.ImageField(max_length=100, upload_to='medicine')
    quantity = models.IntegerField(null=True)


# Patients/User Accounts
class Registration(AbstractUser):
    user_type = [
        ('P', 'Patient'),
        ('A', 'Administration'),
    ]

    sex = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    yorn = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    birthday = models.DateField(null=True)
    phoneNumberRegex = RegexValidator(regex = r"^(09|\+639)\d{9}$")
    c_number = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True)
    address = models.CharField(max_length=300)
    user_type = models.CharField(max_length=30, choices= user_type, verbose_name='user_type', default ='A')
    # Additonal 13/12/22
    cs = models.CharField(max_length=300,null=True)
    sex = models.CharField(max_length=300,null=True,choices= sex, verbose_name='sex')
    philhealth_status = models.CharField(max_length=300,null=True)
    philhealth_number = models.IntegerField(null=True)
    head_of_fam = models.CharField(max_length=300,null=True)
    covid_vacc_status = models.CharField(max_length=300,null=True)
    tobacco_use = models.CharField(max_length=300,null=True)
    bp = models.CharField(max_length=30,null=True)
    temp = models.CharField(max_length=30,null=True)
    pr = models.CharField(max_length=300,null=True)
    rr = models.CharField(max_length=300,null=True)
    wt = models.CharField(max_length=300,null=True)
    ht = models.CharField(max_length=300,null=True)
    bmi = models.CharField(max_length=300,null=True)
    pwd = models.CharField(max_length=300,null=True,choices= yorn, verbose_name='yorn')
    senor = models.CharField(max_length=300,null=True,choices= yorn, verbose_name='yorn')
    injury = models.CharField(max_length=300,null=True,choices= yorn, verbose_name='yorn')
    mental_health = models.CharField(max_length=300,null=True,choices= yorn, verbose_name='yorn')



#Patient Record
class Patient_Record(models.Model):
    patient = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date = models.DateField()
    history_illness = models.CharField(max_length=300)
    physical_exam = models.CharField(max_length=300)
    assessment = models.CharField(max_length=300)
    treatment_or_management_plan = models.CharField(max_length=300)



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