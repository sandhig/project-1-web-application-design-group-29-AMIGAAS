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

- [Python](https://www.python.org/)
- [HTML/CSS](https://html.com/)
- [JavaScript](https://www.javascript.com/)
- [React](https://react.dev/)
- [Node.js](https://nodejs.org/en)
- [Pytest](https://docs.pytest.org/en/stable/)
- [Playwright](https://playwright.dev/)
- [AWS](https://aws.amazon.com) 

### Resources

- [Chatgpt](https://chatgpt.com/)

### Getting Started 

- Clone this repo using : https://github.com/UofT-ECE444-Fall2024/project-1-web-application-design-group-29-AMIGAAS.git.
- Move to appropriate folder : cd <YOUR_PROJECT_NAME>.
- Install pre-requisites. 
- Start coding!

## File Structure 

```sh
PROJECT1-WEB-APPLICATION-DESIGN-GROUP-29-AMIGAAS:.
|   .gitignore
|   CODE_OF_CONDUCT.md
|   CONTRIBUTION.md
|   db.sqlite3
|   dump.rdb
|   package-lock.json
|   package.json
|   README.md   
+---backend
|   |   .DS_Store
|   |   .gitignore
|   |   django_debug.log
|   |   manage.py
|   |   requirements.txt  
|   +---apps 
|   |   +---private_messaging
|   |       |   admin.py
|   |       |   apps.py
|   |       |   consumers.py
|   |       |   models.py
|   |       |   routing.py
|   |       |   serializers.py
|   |       |   tests.py
|   |       |   urls.py
|   |       |   views.py
|   |       |   __init__.py          
|   |   +---products
|   |       |   admin.py
|   |       |   apps.py
|   |       |   models.py
|   |       |   serializers.py
|   |       |   tests.py
|   |       |   test_image_textbook.jpg
|   |       |   urls.py
|   |       |   views.py
|   |       |   __init__.py
|   |   +---profiles
|   |       |   admin.py
|   |       |   apps.py
|   |       |   models.py
|   |       |   serializers.py
|   |       |   tests.py
|   |       |   test_profile_pic.jpg
|   |       |   urls.py
|   |       |   views.py
|   |       |   __init__.py              
|   \---toogoodtothrow
|       |   asgi.py
|       |   settings.py
|       |   urls.py
|       |   wsgi.py
|       |   __init__.py
+---frontend       
|   +---public
|   |   |   favicon.ico
|   |   |   index.html
|   |   |   logo192.png
|   |   |   logo512.png
|   |   |   manifest.json
|   |   |   profile-icon.jpg
|   |   |   robots.txt
|   |   |   uoft-logo4.png
|   |   \---images
|   |       |   logo-icon.png
|   |       |   logo-white.png
|   |       |   logo.png
|   |       |   no-image-icon.png
|   |       |   profile.png
|   |       |   
|   |       \---carousel
|   |               1.png
|   |               2.png
|   |               3.png         
|   \---src
|       |   App.css
|       |   App.js
|       |   App.test.js
|       |   index.css
|       |   index.js
|       |   logo.svg
|       |   reportWebVitals.js
|       |   setupTests.js
|       +---components
|       |   |   Header.css
|       |   |   Header.js
|       |   |   HeaderPre.js
|       |   |   PrivateRoute.js
|       |   |   UploadAndDisplayImage.js   
|       |   \---screens
|       |       |   HomeScreen.js
|       |       |   PrivateMessage.css
|       |       |   PrivateMessaging.js
|       |       |   WelcomePage.css
|       |       |   WelcomePage.js     
|       |       +---products
|       |           |   CreateListing.css
|       |           |   CreateListing.js
|       |           |   ProductEdit.js
|       |           |   ProductListing.css
|       |           |   ProductListing.js
|       |           |   Products.css
|       |           |   Products.js
|       |           |   ProductView.js
|       |           |   SearchResults.js
|       |           |   Wishlist.css
|       |           |   Wishlist.js   
|       |       +---profiles
|       |           |   EditProfile.css
|       |           |   EditProfile.js
|       |           |   EmailVerification.js
|       |           |   UserProfile.css
|       |           |   UserProfile.js
|       |           |   UsersLogin.js
|       |           |   UsersLogOut.js
|       |           |   UsersSignUp.css
|       |           |   UsersSignUp.js
|       +---context
|       |       UserContext.js
|       \---tests
|               test_products.py
```

## Contributing

Please see [CONTRIBUTION.md](/CONTRIBUTION.md). 
