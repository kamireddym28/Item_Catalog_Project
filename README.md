# Item Catalog Project -- FSDN Project4

 > The objective of this project is to develope a RESTful web application using Python Flask framework.  
 
## About
Database of items and its models is created which can be accessed by using SQL. Implemented third part OAUTH2 authentication using Google and Facebook sign in on the application. Users can perform CRUD (Create, Read, Update and Delete) operations by logging in to the application.

## Requirements

 - [**Python 2.7** or **Python 3.6**](https://www.python.org/downloads/)
 - [**Vagrant**](https://www.vagrantup.com/)
 - [**VirtualBox**](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

## Usage

 - Install either of the python versions from the URL provided
 - Install the VirtualMachine(VM) to run an SQL database server using the tools provided*
 - [Download](https://github.com/kamireddym28/Item_Catalog_Project.git) or clone this repository and unzip it
 - Place the unziped file in vagrant folder on local computer
 - Bring the VM online 
 - Load the database by ``` cd ``` into the ``` vagrant ``` directory
 - Set the path to the newsdata.sql inside the vagrant directory  
 - Execute the ***database_setup.py*** file using ``` python newsdatadb.py ```
 - Execute the ***modelcatalog.py*** file using ``` python modelcatalog.py ```
 - Execute the ***Catalog_project.py*** file using ``` python Catalog_project.py ```
 - On succesful execution, application can be accessed at ***http://localhost:5000*** 
 - Use ``` CTRL+D ``` to exit the VM

## Description of files

 - ***Catalog_project.py*** : Code that enables CRUD functionality, API endpoints       and routing, OAUTH2 iplementation functionality can be found here
 - ***database_setup.py*** 	: To setup smartphone application database 
 - ***modelcatalog.py*** 	: DB containing various smartphones and their correponding models
 - **static folder** : CSS and images used in this appliction are placed here
 - **template folder** : HTML files to present this application aesthetically can be found here
 - ***client_secrets.json*** and ***fb_client_ectrets.json*** : JSON files to enable OAUTH2 implementation using google and facebook sign in respectively 
			     
## Commands 
 - Bring the VM online using ``` vagrant up ``` 
 - Log into VM using ``` vagrant ssh ```

## Courtesy

 Full Stack foundations and Authentication and Authorization courses were provided by Udacity

 #### Note:
 
 - Vagrant and VirtualBox are the tools to install and manage the VM*
 - OAUTH2 implementation using google and facebook can done by registering the application in [google developer tools](https://developers.google.com/) and [facebook developer tools](https://developers.facebook.com/)
 - Replace the google and facebook client id and secret keys with yours where ever needed
 
 

