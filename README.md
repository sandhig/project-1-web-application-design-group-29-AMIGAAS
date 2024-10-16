# ECE444 - UofT Second Hand Hub Web Application Development

## About the Project 

We are building U of T Second Hand Hub; a website application designed by students for students where they can browse and sell secondhand items within the U of T community.  

## Table of Contents

1. [About the Project](#about-the-project)
2. [Project Purpose](#project-purpose)
3. [Development Environment](#development-environment)
4. [File Structure](#file-structure)
5. [Contributing](#contributing)

## Project Purpose

The purpose of this project is to design and launch a web application. 

## Development Environment

We will be developing our website application in VS code. 

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=15896031&assignment_repo_type=AssignmentRepo)

We will be maintaining our codebase on [GitHub.](https://github.com/UofT-ECE444-Fall2024/project-1-web-application-design-group-29-AMIGAAS)

We will be tracking our progress, report bugs and fixes, as well as maintain an up-to-date list of tasks to be accomplished in each sprint on [Jira](https://amigaas.atlassian.net/jira/software/projects/SCRUM/boards/1)

### Requirements 

- Python 
- Flask 
- HTML/CSS
- JavaScript
- Flake8
- Black 
- Pytest

### Getting Started 

- Clone this repo using : https://github.com/UofT-ECE444-Fall2024/project-1-web-application-design-group-29-AMIGAAS.git.
- Move to appropriate folder : cd <YOUR_PROJECT_NAME>.
- Install pre-requisites. 
- Start coding!

## File Structure 

TBD. 

## Contributing

Please see [CONTRIBUTION.md](/CONTRIBUTION.md). 

--------

# Setup (delete later -- Amy)

## Cloning the repository

First step is to create a new branch for your work. Make sure to create the branch off of *django-setup*! Then, clone the repo onto your local machine if you haven't already. To do so, open a terminal and run:
```
git clone https://github.com/UofT-ECE444-Fall2024/project-1-web-application-design-group-29-AMIGAAS.git
```

Next, open the project in VS Code and switch to your branch. Now we're ready to start coding :)

## Running the application

First let's test if you're able to run the application as is locally.

### In one terminal:

Start a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install everything:
```
pip install -r requirements.txt
```

Start the backend:
```
cd backend
python3 manage.py runserver
```

### In another terminal:

Start the frontend:
```
cd frontend
npm start
```

You will likely need to install Node.js if you haven't used it before. Download the prebuilt installer from [here](https://nodejs.org/en/download/prebuilt-installer). Once you're able to run ```npm -v``` in your terminal, you're ready to go!

## Starting development

Let's walk through the creation of a product. I've already completed all of these steps in the django-setup branch, so you should be see all of the files I'm about to mention in your local branch.

## Backend

### Create a new table in the database

Navigate to backend/apps. This is where all of our "apps" are stored (in Django, an app is a component of the project). To create a new app, run:
```
python manage.py startapp products
```

Next, navigate to backend/toogoodtothrow/settings.py and find the INSTALLED_APPS list. Add the new app to the list as ```'apps.products'``` (the "apps." is required because we created the products app inside the "apps" folder).

Now go back to backend/apps/products. You should see a file called models.py. This is where we'll define our table in the database! Create a new class as follows:
```
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Add more table columns here!

    def __str__(self):
        return self.name
```

Check out [this](https://www.geeksforgeeks.org/django-model-data-types-and-fields-list/) link for all of the field types you can use when defining a new table column. Note that Django automatically adds an ID column as the primary key, so we don't have to worry about that!

Table looks good? It's time to migrate these changes to the database. Run:
```
python manage.py makemigrations
python manage.py migrate
```

### Create a Django API

Great we're almost finished with the backend! Let's create an API to read and write data from the table we just made. Create a new file in backend/apps/products called serializers.py (this will be used to handle JSON conversion). Add the following to this file:
```
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

Add the following to views.py to handle the GET and POST HTTP requests:
```
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Create another new file called urls.py. Add the following:
```
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
]
```

Finally, head to backend/toogoodtothrow/urls.py and add a new path to the urlpatterns list:
```
path('api/', include('apps.products.urls'))
```

Remember to include the "apps." in the path name!

### Check the database

Now we're finished setting up the backend! Let's connect to the database and see if our table was created. Open a terminal and run:
```
psql -h database-1.cvy8o4eg6hpb.us-east-2.rds.amazonaws.com -U postgres -p 5432
```

The password is ```sppA2VDWWAK3O4q7CF9i```.

To list all tables, run ```\dt```.

To view a table, run ```\d products_product``` where products_product is the table name.

To view all rows in a table, run ```SELECT * FROM products_product``` (or whatever query you'd like :D).

To exit the database, run ```\q```.

## Frontend

Let's create a way for the users to add to and view the database entries! Navigate to frontend/src/components and create a new file called Products.js. I've put some functions in there to read from and write to the database. To learn more, search "react axios" (or just ask ChatGPT - that's what I did lol).

Finally, add the following to App() in frontend/src/App.js:
```
return (
  <div className="App">
    <Products />
  </div>
);
```

That's it! Let me know if you have any questions :)
