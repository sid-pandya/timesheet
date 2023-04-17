# Flask Time Sheet Web App

This is a web application built with Python and Flask for managing time sheets. It allows users to view, add, and remove time entries for a given week.

# Features
- View time entries for the current week
- Navigate to previous and next weeks
- Add new time entries
- Remove existing time entries
- Submit time entries to a database

# Getting Started
To run the web app locally, follow these steps:

- Clone the repository to your local machine
- Install the required dependencies by running pip install -r requirements.txt
- Set up a database to store time entries (SQLite is used by default)
- Run the app with flask run

# Usage. 

Once the app is running, navigate to http://localhost:5000 in your web browser to view the current week's time entries. Use the "Previous Week" and "Next Week" buttons to navigate to different weeks.
To add a new time entry, fill out the "Time In" and "Time Out" fields in the table and click the "Add" button. To remove an existing time entry, click the "Remove" button next to the entry.
To submit time entries to the database, click the "Submit" button below the table. This will make a POST request to the API endpoint /submit with a JSON string containing the time entries. The server will then save the time entries to the database.

# API
The following API endpoints are available:

- /submit (POST): submit time entries to the database

# Technologies Used
- Python
- Flask
- SQLite
- JavaScript
- HTML
- CSS

## Video Walkthrough
Here's a walkthrough of implemented user stories:

<img src='http://g.recordit.co/Q5DdQx20H0.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />
