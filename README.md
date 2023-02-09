# option-blocks-website
 
# SETTING UP THE WEBSITE

NOTE!
.env file needs to be created with these attributes definied. This is to ensure sensitive information is not
easily accessible

SECRET_KEY=*KEY GOES HERE* *this should be a long string with a mix of characters and symbols*
*use this for fallback 'django-insecure-2w5ds_fm49w!kjc2o^16ri!w(u!t8s#7arptsbyes#8(jo82h'*
DJANGO_DEBUG=True
DATABASE_URL=postgresql://postgres:*POSTGRESPASSWORD*@@localhost:5432/option-block-db

*PASSWORD CAN BE PROVIDED BY ME LATER*

1) create a new python virtual environment if required

tells python 'use module venv (module for creating virtual envs) as name it ...'
py -m venv *name of env*
e.g.
py -m venv env

2) activate the virtual environment

*name of env*\Scripts\activate.bat

env\Scripts\activate.bat

3) install requirements
In general: 
pip install -r /path/to/requirements.txt

if you are in the directiory of the requirements folder
For our case:
'pip install -r requirements.txt'

4) Ensure that you are in the directory with manage.py (which is in the same directory as requirements.txt)

5) Migration checks
Run the following commands in order to check the database is running

'py manage.py makemigrations' # find migrations
'py manage.py migrate' # commit migrations

5.2) optional sys check

'py manage.py check' # system check

6) Create a superuser 

'py manage.py createsuperuser'

You will recieve a prompt to create a super user.
Follow the instructions and set a password and username you will
remember. THIS IS IMPORTANT to access the admin.

7) run in cmd 'py manage.py runserver'
This will run the development server
Ensure no errors are raised.

8) Check the CMD and see the URL the server is running on.