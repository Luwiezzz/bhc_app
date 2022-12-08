from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import redirect, render
#from pyexpat.errors import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from .models import *

import os

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Q
from datetime import date, datetime
import datetime

from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
installed_apps = ['dhc_app']

#Login
def index(request):
    news = News_and_Updates.objects.all()
    form = PatientsRegistration()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password) 
        print(user)
        if user is not None and user.user_type == 'P':
            login(request, user)
            return redirect('/patient_dashboard')
        else:
           messages.error(request, 'User is not found!')
           return redirect('/index')

    context =  {'form': form, 'news': news }
    return render(request, 'bhc_app/index.html', context)


#Sign Up
def registration(request):
    if request.method == 'POST':
        form = PatientsRegistration(request.POST)
        if form.is_valid():
            form.instance.user_type = 'P'
            form.save()
            messages.success(request, 'Created Account Successfullly!')
            return redirect ('/index')
        else:
           messages.error(request, 'Invalid Credentials!')
           return redirect('/index')

    return render(request, 'bhc_app/index.html')


#Log Out
def logout_user(request):
    logout(request)
    return redirect('/index')








#patients pages

def patient_dashboard(request):
    user = request.user
    form = PasswordChangeForm(request.user)
    return render(request, 'bhc_app/patient_dashboard.html', {'form': form, 'user': user})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/patient_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('/patient_dashboard')


def change_information(request):
    user = request.user
    if request.method == 'POST':
        patients = Registration.objects.get(username=user.username)
        patients.first_name = request.POST.get('first_name')
        patients.last_name = request.POST.get('last_name')
        patients.c_number = request.POST.get('c_number')
        patients.birthday = request.POST.get('birthday')
        patients.address = request.POST.get('address')
        patients.username = request.POST.get('username')
        patients.save()
        messages.success(request, 'Your information was successfully updated!')
        return redirect('/patient_dashboard')


def delete_account(request):
    user = request.user
    if request.method == 'POST':
        patients = Registration.objects.get(username=user.username)
        patients.delete()
        messages.error(request, 'Your account was successfully deleted!')
        return redirect('/index')


def patient_doctor(request):
    doc = Doctors.objects.all()
    context = {
    'doc': doc
    }
    return render(request, 'bhc_app/patient_doctor.html', context)

#Patient Appointment
def patient_set_appointment(request):
    appoint = Appointment.objects.filter(patient=request.user.id)
    current_week = date.today().isocalendar()[1]
    appoint1 = Appointment.objects.filter(Q(patient=request.user.id) & Q(date__week=current_week))
    context = {
    'appoint': appoint,
    'appoint1': appoint1
    }
    return render(request, 'bhc_app/patient_set_appointment.html', context)


def patient_set_appointment_submit(request):
    # Date for the weeks
    date1 = datetime.datetime.today()
    start_week = date1 - datetime.timedelta(date1.weekday())
    end_week = start_week + datetime.timedelta(7)
    print(start_week)
    print(end_week)
    if request.method =='POST':
        # Uers Inputs
        date2 = request.POST.get('date')
        date3 = datetime.datetime.strptime(date2, "%Y-%m-%d") 
        time = request.POST.get('time')
        reasons = request.POST.get('reasons')
        if start_week <= date3 <= end_week:
            doctor = Appointment.objects.create( patient=request.user, date=date3, time=time, reasons=reasons)
            doctor.save()
            messages.success(request, 'Success!')
            return redirect('/patient_set_appointment')
        else:
            messages.error(request, 'Must input Date for this week only!')
            return redirect('/patient_set_appointment')
    return redirect('/patient_set_appointment')

#Patient Medicine
def patient_medicine(request):
    med = Medicine.objects.all()
    context = {
    'med': med
    }
    return render(request, 'bhc_app/patient_medicine.html', context)

#Patient - News and Updates
def patient_news_and_update(request):
    news = News_and_Updates.objects.all()
    context = {
    'news': news
    }
    return render(request, 'bhc_app/patient_news_and_update.html', context)

def sendalert(request):
    if request.method =='POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        location = request.POST.get('location')
        message1 = 'Sender: ' + email + '⧵n' + message + " " + "Here's my address/current location -->" + " " + location
        send_mail(subject, 
            message1, email , [settings.EMAIL_HOST_USER], fail_silently=False)
        messages.success(request, 'Successfully Send Alert!')
        return redirect('/patient_dashboard')


#admin_login
def administrator(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password) 
        if user is not None and user.user_type == 'A':
            login(request, user)
            return redirect('/admin_homepage')
        else:
           messages.error(request, 'User is not found!')
    return render(request, 'bhc_app/administrator.html')  


#admin_homepage
def admin_homepage(request):
    return render(request, 'bhc_app/admin_homepage.html')

#Admin - Doctor
def admin_doctor(request):
    doc = Doctors.objects.all()
    context = {
    'doc': doc
    }
    return render(request, 'bhc_app/admin_doctor.html', context)

def doctor_add(request):
    if request.method =='POST':
        picture = request.FILES.get('picture', "blank.jpg")
        name = request.POST.get('name')
        if Doctors.objects.filter(name = name).exists():
            messages.error(request, 'Doctor Name is already existed')
            return redirect('/admin_doctor')
        else:
            position = request.POST.get('position')
            specialty = request.POST.get('specialty')
            status = request.POST.get('status')
            doctor = Doctors.objects.create(picture=picture, name=name, position=position, specialty=specialty, status=status)
            doctor.save()
            return redirect('/admin_doctor')

def doctor_edit(request, id):
    if request.method =='POST':
        edit= Doctors.objects.get(id=id)
        # edit.picture = request.FILES.get('picture', 'blank.jpg')
        edit.name = request.POST.get('name')
        edit.position = request.POST.get('position')
        edit.specialty = request.POST.get('specialty')
        edit.status = request.POST.get('status')
        edit.save()
        return redirect('/admin_doctor')

def doctor_del(request,id):
    doc = Doctors.objects.get(id=id)
    doc.delete()
    return redirect('/admin_doctor')


#Admin - Medicine
def admin_medicine(request):
    med = Medicine.objects.all()
    context = {
    'med': med
    }
    return render(request, 'bhc_app/admin_medicine.html', context)

def medicine_add(request):
    if request.method =='POST':
        picture = request.FILES.get('picture', "blank.jpg")
        name = request.POST.get('name')
        if Medicine.objects.filter(name = name).exists():
            messages.error(request, 'Medicine Name is already existed')
            return redirect('/admin_medicine')
        else:
            dosage = request.POST.get('dosage')
            medicine_type = request.POST.get('medicine_type')
            quantity = request.POST.get('quantity')
            meds = Medicine.objects.create(picture=picture, name=name, dosage=dosage, medicine_type=medicine_type, quantity=quantity)
            meds.save()
        return redirect('/admin_medicine')

def medicine_edit(request, id):
    if request.method =='POST':
        edit= Medicine.objects.get(id=id)
        edit.name = request.POST.get('name')
        edit.dosage = request.POST.get('dosage')
        edit.medicine_type = request.POST.get('medicine_type')
        edit.quantity = request.POST.get('quantity')
        edit.save()
        return redirect('/admin_medicine')

def medicine_del(request,id):
    doc = Medicine.objects.get(id=id)
    doc.delete()
    return redirect('/admin_medicine')


#Admin - Appointment
def admin_appointment(request):
    appoint = Appointment.objects.all()
    current_week = date.today().isocalendar()[1]
    appoint1 = Appointment.objects.filter(date__week=current_week)
    context = {
    'appoint': appoint,
    'appoint1': appoint1
    }
    return render(request, 'bhc_app/admin_appointment.html', context)




#Admin - News and Updates
def admin_news_and_update(request):
    news = News_and_Updates.objects.all()
    context = {
    'news': news
    }
    return render(request, 'bhc_app/admin_news_and_update.html', context)

def news_add(request):
    if request.method =='POST':
        news_and_updates = request.FILES.get('news_and_updates', "blank.jpg")
        headline = request.POST.get('headline')
        fb_link = request.POST.get('fb_link')
        news = News_and_Updates.objects.create(news_and_updates=news_and_updates, headline=headline, fb_link=fb_link)
        news.save()
        return redirect('/admin_news_and_update')

#Admin - Staff
def admin_staff(request):
    if Staff.objects.count() > 0 :
        staff = Staff.objects.latest('id')
        context = {'staff': staff}
        return render(request, 'bhc_app/admin_staff.html', context)
    else:
        staff = Staff.objects.all()
        context = {'staff': staff}
        return render(request, 'bhc_app/admin_staff.html', context)

def staff_update(request):
    if request.method =='POST':
        staff_picture = request.FILES.get('staff_picture')
        year = request.POST.get('year')
        staff = Staff.objects.create(staff_picture=staff_picture, year=year)
        staff.save()
        return redirect('/admin_staff')


      
#Admin - Patients/Users
def admin_patients(request):
    users = Registration.objects.filter(user_type='P')
    context = {
    'users': users
    }
    return render(request, 'bhc_app/admin_patients.html', context)

#Admin - Patients/Users History
def admin_patient_history(request,id):
    appoint = Appointment.objects.all()
    context = {
        'appoint': appoint
    }
    return render(request, 'bhc_app/admin_patient_history.html', context)

