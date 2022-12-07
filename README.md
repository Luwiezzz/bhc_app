# bhca


1. Open Gitbash
- Type: git pull

2. Open Xampp MySQL Admin
-Drop all bhc tables

3. Open bhc_app/migrations folder
- delete the 00001.py file

4. Open terminal(powershell)
-Type:
cd bhc_project
py manage.py makemigration
py manage.py migrate
py manage.py createsuperuser
-Fill username, email and password
py manage.py runserver



Install

pip install django-phonenumber-field[phonenumbers]




5. Go to browser
-Patient Page Go to:
http://127.0.0.1:8000/


-BHC Admin Page Go to:
http://127.0.0.1:8000/admin_login


-Django Admin Page Go to:
http://127.0.0.1:8000/admin
