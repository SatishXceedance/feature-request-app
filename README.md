# Technologies and database:
Database: 
•sqlite

Back-end:  
•python >= 3.0  
•django 2.0.3   
•django-rest-framework  

Front-end:  
•HTML  
•CSS  
•bootstrap  
•JavaScript  
•jquery  
•knockout js   
•Jquery.datatTable  

	
# Steps to run the application

```

# Install virtualenv in your system
$ python3 -m pip install --user virtualenv (For macOS and Linux)
$ py -m pip install --user virtualenv (For Windows)


# Create virtual environment
$ python3 -m virtualenv env (For macOS and Linux)
$ py -m virtualenv env (For Windows)

# Activate virtual environment
$ source env/Scripts/activate (For macOS and Linux)
$ .\env\Scripts\activate (For Windows)

# Get project code form github
$ git clone https://github.com/SatishXceedance/feature-request-app.git

# Go to the project directory
$ cd feature-request-app

# Install project dependencies from requirements.txt file
$ pip install -r requirements.txt

# For getting database tables 
$ python manage.py migrate

# Runserver on your local system
$ python manage.py runserver

# Go to the browser and open http://127.0.0.1:8000/

# To stop server press ctrl+C

# Run Test cases
$ python manage.py test

# to deactivate the virtual environment
$ deativate

```
