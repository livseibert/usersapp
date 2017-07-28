# Cavatica User Data App

This app takes cavatica_users.csv files and displays the data in a more readable way.

## Prerequisites
* Python 2.7
* Download desired cavatica_users.csv files from the Cavatica database, making sure there is one for each day

Requirements found in `requirements.txt`:
* Flask
* Matplotlib


## Installing

To get a copy of this project up and running on your machine, download it from this link: https://github.com/livseibert/usersapp.git

### Configuration

The app needs to know the local folder containing the cavatica_users.csv files and the folder to store static content. Update the `DATA_PATH` and `STATIC_PATH` variables in `views.py` as appropriate.

## How To

To run this app, type export FLASK_APP=views.py, then flask run in the terminal and copy the link into a web browser.
The first page of this app displays a form that allows the user to enter a range of dates. There must be csv files for all the dates in this range in order for the app to work properly. Upon submitting this form, a chart is generated showing the number of users on each day. A graph also displays the chart's information in a more visual way. Clicking the date in the chart leads to the next page, where detailed information about each user on that day is available. 

Clicking the header of each column sorts the data by the information in that column, and it toggles between ascending and descending order.
