# option-blocks-website

# POSTGRES SETUP
postgres will run locally on the machine and will need to be installed  

# download

1) Go the postgres website and find the downloads page. 

2) Select the installation for windows.

3) Download version 14.7 (2019, 2016) for windows x86-64.

4) Once downloaded, load the exe file and follow the steps. 

# config

5) Choose where you would like to install postgres

6) Install all components to download. Ensure PgAdmin 4 is selected!

7) Choose where you would like to store your data 

8) Create your own master password. REMMEMBER THIS FOR LATER! PgAdmin will need this for later

9) Define port. 5432 should be used.

10) Select default Locale 

11) Start the download 

12) Once the download is completed, stack builder will automatically open, you can close this and 
open up PgAdmin 4.

# PgAdmin 4

13) When you enter PgAdmin, it will prompt for the master password, enter the password you defined
in the configuration 

14) On the left of the screen, click on the 'Servers' in the browsers section to open the available servers

15) Then click on postgreSQL 14 and open it up

16) The right click on databases and click on create to create a new database. Give the database a name. This will be important later
in the Django config.

Once a database has been created it will automatically start running and be ready for use.

# PYTHON SERVER (DJANGO) SETUP

# VIRTUAL ENVIRONMENT SETUP AND INSTALLING PACKAGES

1) create a new python virtual environment if required

tells python 'use module venv (module for creating virtual envs) and name it ...'
py -m venv <name-of-env>
e.g.
py -m venv env

2) activate the virtual environment

<name-of-environment>\Scripts\activate.bat
e.g.
env\Scripts\activate.bat

3) install requirements in the command line
In general: 

pip install -r /path/to/requirements.txt

if you are in the directiory of the requirements folder
For our case:
'pip install -r requirements.txt'

4) ENSURE YOU ARE IN THE CURRENT WORKING DIRECTORY WHERE THE SERVER IS STORED
e.g. you are in the same directory as the 'manage.py' file

# ENVIRONMENT FILE .env
.env file needs to be created with these attributes definied. This is to ensure sensitive information is not
easily accessible.
--------------------------------------------------------------------------------
SECRET_KEY=*KEY GOES HERE* *this should be a long string with a mix of characters and symbols*
*use this for fallback 'django-insecure-2w5ds_fm49w!kjc2o^16ri!w(u!t8s#7arptsbyes#8(jo82h'*

DJANGO_DEBUG=True

*follow this URL configuration and replace any <>*

DATABASE_URL=postgresql://postgres:<password-to-db>@localhost:<port>/<name-of-database>
--------------------------------------------------------------------------------

the <password-to-db> is the master password you have defined
the <port> is 5432 or otherwise if defined differently in install config or in admin
<name-of-database> points to the database you have just created


5.1) Migration and system checks
Run the following commands in order to check the database is running

'py manage.py makemigrations' # find migrations
'py manage.py migrate' # commit migrations

5.2) optional sys check but is recommended

'py manage.py check' # system check

6) Create a superuser 

'py manage.py createsuperuser'

You will recieve a prompt to create a super user.
Follow the instructions and set a password and username you will
remember. THIS IS IMPORTANT to access the admin.

7) run in cmd 'py manage.py runserver <IP-address>:<Port>'

The <IP-adrress> will need the internal school IP address not the public network IP address
The <Port> should be '8080' It can be defined otherwise but the frontend will need to be reconfigured to point to this new URL port

This will run the development server
Ensure no errors are raised.

8) Check the CMD and see the URL the server is running on.

# SHUT DOWN

9) Ctrl-C on the CMD where the server is running will turn it off. You can also close the terminal.

optional cleanup

10.1) turnning off virtual environment 

<name-of-environment>\Scripts\deactivate.bat
e.g.
env\Scripts\activate.bat

NOTE: The database will automatically shutdown after all sessions have stopped e.g. no more transactions to the database
have been executed. 
Postgres will terminate all its services if power to the host device is lost when running locally. 