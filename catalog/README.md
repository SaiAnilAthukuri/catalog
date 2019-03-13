# Item Catalog Web App
By Athukuri Sai Anil
This web app is a project for the Udacity [Full Stack Web Developer Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## In This Project
*This project has one main Python module `main.py` which runs the Flask application.
*A SQL database is created using the `mobile_Setup.py` module and you can populate the database with test data using `mobiledata_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills Required
Python,HTML,CSS,OAuth,Flask Framework,DataBaseModels,JavaScript,.net 


## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install
1. Install Vagrant & VirtualBox 
2. step 1:I have done Vagrant VM('vagrant init')
  install flask -application and i done  vagrant init ubuntu/Xenial64
3. step 2:i have done  Vagrant VM (`vagrant up`)
4. step 3:I have done Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run pip install requests
Or you can simply Install the dependency libraries (Flask, sqlalchemy, requests,psycopg2 and oauth2client) by running 
`pip install -r requirements.txt`
7. Setup application database `python /mobile-store/mobile_Setup.py`
8. Insert sample data `python /mobile-store/mobiledata_init.py`
9. Run application using `python /mobile-store/main.py`
10. Access the application locally using http://localhost:8888

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Mobile_Store'
7. Authorized JavaScript origins = 'http://localhost:8888'
8. Authorized redirect URIs = 'http://localhost:8888/login' && 'http://localhost:8888/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in book-store directory that you cloned from here
14. Run application using `python /mobile_store/main.py`


##  Small  introduction
In this project 3 python files are present
They are 
1. main.py`
2.mobile_setup.py
3.mobiledata_init.py


## templates
1.addMobileCompany.html
2.addMobileDetails.html
3.admin_login.html
4.admin_loginFail.html
5.allMobiles.html
6.deleteMobile.html
7.deleteMobileCategory.html
8.editMobile.html
9.editMobileCategory.html
10.login.html
11.mainpage.html
12.myhome.html
13.nav.html
14.sample.html
15.showMobile.html

## JSON Endpoints
The following are open to the public:

allMobilesJSON: `/MobileStore/JSON`
    - Displays the whole mobiles models catalog. mobile Categories and all models.

categoriesJSON: `/MobileStore/mobileCategories/JSON`
    - Displays all Mobile categories
itemsJSON: `/MobileStore/mobiles/JSON`
	- Displays all Mobile Models

categoryItemsJSON: `/MobileStore/<path:mobile_name>/mobiles/JSON`
    - Displays mobile models for a specific Mobile category

ItemJSON: `/MobileStore/<path:mobile_name>/<path:edition_name>/JSON`
    - Displays a specific Mobile category Model.

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
