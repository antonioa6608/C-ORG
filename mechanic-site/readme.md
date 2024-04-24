# Readme

## Create and activate virtual environment (optional)

To create a virtual environment run:

    python -m venv env

Then activate it with:


`./env/Scripts/activate`    (powershell)



## Install The project

The projects and it's dependancies can be installed with: manually 
pip install flask 
pip install Google-Images-Search
pip install pytest
pip install windows-curses

  

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



