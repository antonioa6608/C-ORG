# C-ORG ![interface](https://github.com/antonioa6608/C-ORG/assets/90696477/655fb716-7db8-4e6d-ab8f-2acbf5603f32)


<h1>Autobookr</h1>
<p> Autobookr is a web based app that connects customers and mechanics that facilitates the booking process in a easier way. How does it work?
Autobookr uses user zipcode to find mechanics near the area to book a appointment. Customer will input basic information such as name,contact,issue with vehicle.To select a date, autobookr will provide a calender to choose which days are available per mechanic schedule. Sending information to mechanic that will allow to view their schedule or make any changes regarding customer appointment.
![AutoBookrr (1)](https://github.com/antonioa6608/C-ORG/assets/90696477/a487e784-d8e2-4287-9eb3-f189cef928ce)

</p>
<h1> GOOGLE MAP USAGE Testing purposes only </h1>
<p> Click on the Flask.Auth use the python app.py command to run the program. When acess the web type the zip code but if you want a specific location type state, city, zip code, and 
street then zoom in and it should show.  </p>

## MUST HAVE THE CORRECT PATH IN YOUR SYSTEM VARIABLES SINCE 'python not found' when running application. 

## Installations
<p> 1.Python
2. Flask
In terminal run to see the latest version of python and pip. We used the latest version of python </p>
`python --version`
`pip --version`

## Accessing AutoBookr 
<p>Clone the CORG in Github, once its clone open up vscode studio .  The website is located in the mechanic-site folder. Open up the terminal window. type in CD C-ORG/mechanic-site to navigate to the correct folder. follow the steps to activate environment, install dependencies, run the application. 
</p>


## Create and activate virtual environment (optional)

To create a virtual environment run:

    python -m venv env

Then activate it with:


`./env/Scripts/activate`    (powershell)terminal vscode 



## Install The project

The projects and it's dependancies can be installed with: MANAULLY 
`pip install flask`
`pip install Google-Images-Search`
`pip install pytest`
`pip install windows-curses`
`pip install werkzeug`

## we used sqlite3 for the database. link to download , standard installer depending on what type of operating system in your machine 
https://sqlitebrowser.org/dl/
## locate the schema.sql to open it up in the DB BROWSER(SQLITE). schema.sql located in mechanic_site folder

## Initialising the database

The projects database must be initialised before the project can be run (this only needs to happen once, running again will reset the database).

    flask --app mechanic-site init-db 

## Adding Fake Data (Optional)

The project might look a bit empty at first, so I added a command to fill america with fake mechanics for testing purposes. If you want to fill your database with some faked testing data you can run the command but it might take around a minute or two:

    flask --app mechanic-site populate-db
    
## Running The app

Run the server with

    flask --app mechanic_site run --debug

Then open the address it is running on in a browser.

## Run Unit Tests

You can run the unit tests with:

`pytest`





