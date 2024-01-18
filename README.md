# Python recipe app (Django version)

**Table of content**

- [Project description](#project-description)
- [User interfaces](#user-interfaces)
- [Technical aspects](#technical-aspects)
- [App dependencies ](#app-dependencies)


## Project description

This project (A tablespoon of discovery - Cuisine Atlas) is a full-stack web application built with Django. This recipe web app was created to serve as a central hub for international cuisine lovers. Users can go on the web app and access many recipes from all around the globe, search for recipes by name or via advanced search, and even submit their own recipe. Users can also create an account for a more complete experience, such as being able to create their own private recipes, add recipes to their favorite and comment recipes publicly.

This web app can be broken down in the five following points:

- **Who** — For any users who would like to access international recipes and try different dishes in a simple and convinient way.
- **What** — A reponsive Django-built web app with registration option, users media files upload and customize user experience, while being installable like a native app on desktop and mobile phones.
- **When** — Users are able to use the Cuisine Atlas whenever they want to search, create or submit recipes.
- **Where** — The Cuisine Atlas is hosted online on Heroku. Users can access the web app on their browser, or install it as a desktop app or mobile app. As it’s responsive, it displays well on any device sizes, whether on computer, tablet or mobile. 
- **Why** — Django has the advantage of being developer friendly, while also being powerful enough to run different types of websites and web applications.

## User interfaces

Two different types of user experience are offered: interfaces for registered users and interfaces for non-registered users. Users choose what they want on the web app home page. 

- **Unregistered users**

Unregistered users have access to the recipes made available by Cuisine Atlas. They can consult each recipe and share them. They can also perform advanced searches, and submit recipes they'd like to share with other users. 

However, they cannot perform any CRUD operations (except for READ).

- **Registered users**

Those who wish to do so can create an account and login to their account. These users can do everything that unregistered users can do, in addition to being able to:

-Comment publicly on recipes  
-Create their own private recipes (profile page)  
-Add recipes to their favorites (profile page)  

## Technical aspects

This Recipe web app is built with Django version 4.2.6, Python version 3.8.7 and a runtime python version 3.9.18 (specified in the directory runtime.txt file) to comply with Heroku stack during production - the plateform used for deployment.

During development, an SQLite database is used. However, since this default SQLite database can’t be used on Heroku (as it’s file based and will be deleted every time the application restarts or if any variables change), the database/service heroku-postgresql is used for production.

Also, even if not part of the final product, QuerySet API, DataFrames (pandas) and plotting libraries (matplotlib - a comprehensive library for creating static, animated, and interactive visualizations in Python) have been tried out during the development of this web app.

The frontend is built with HTML, Bootstrap, CSS and JavaScript.

## App dependencies

The following packages and dependencies are required for the Recipe web app to work (also accessible via the requirement.txt file):

asgiref==3.7.2  
backports.zoneinfo==0.2.1  
cycler==0.12.1  
dj-database-url==2.1.0  
Django==4.2.6  
fonttools==4.44.0  
gunicorn==21.2.0  
kiwisolver==1.4.5  
matplotlib==3.5.2  
numpy==1.24.4  
packaging==23.2  
pandas==2.0.3  
Pillow==10.1.0  
psycopg2-binary==2.8.6  
pyparsing==3.1.1  
python-dateutil==2.8.2  
python-dotenv==1.0.0  
pytz==2023.3.post1  
six==1.16.0  
sqlparse==0.4.4  
typing_extensions==4.8.0  
tzdata==2023.3  
whitenoise==6.6.0  

