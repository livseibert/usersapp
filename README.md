# Cavatica User Data App

This app takes cavatica_users.csv files and displays the data in a more readable way.

## Prerequisites

* Download desired cavatica_users.csv files from the Cavatica database, making sure there is one for each day
* Python 2.7
* Flask 0.10.1
* Matplotlib

## Intalling

To get a copy of this project up and running on your machine, download it from this link: https://github.com/livseibert/usersapp.git

### Necessary Modifications

* views.py line 13, modify url to hold the path to graph.png on your personal computer
* views.py line 34, 59, modify csv_name so that it points to where the data folder that holds the csvs are on your computer
* views.py line 54, modify argument of savefig so that it is the same path as line 13

## How To

To run this app, type export FLASK_APP=views.py, then flask run in the terminal and copy the link into a web browser.
The first page of this app displays a form that allows the user to enter a range of dates. There must be csv files for all
the dates in this range in order for the app to work properly. Upon submitting this form, a chart is generated showing the
number of users on each day. A graph also displays the chart's information in a more visual way. Clicking the date in the chart
leads to the next page, where detailed information about each user on that day is available. Clicking the header of each column
sorts the data by the information in that column, and it toggles between ascending and descending order.
