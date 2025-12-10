To run:npm start
			python -m http.server 3000
			http://localhost:3000/dashboard.html

#This is the frontend for an Excel Upload & Processing System. -It allows users to upload .xlsx files and view processed results in a dashboard.

#Features

#Upload Excel file (.xlsx) -Sends upload request to backend API -Shows upload success/error messages -Dashboard shows: -Total files processed -Approved rows -Rejected rows -Clickable table of uploaded files -Download processed files

#FRONTEND STRUCTURE frontend/ 
│── index.html # File upload page │
── dashboard.html # Dashboard to view processing results │
── style.css # Styling for both pages

🔗 API Endpoints Used -This frontend communicates with a backend running at: http://127.0.0.1:8000

#ENDPOINT:

Action	Method	Endpoint
Upload Excel file	POST	/api/upload
Fetch processed file list	GET	/api/processed-files
Download processed file	GET	/api/download/<filename>
#How to Run Frontend

-run this on terminal : npm start -Download or clone this repository
-Open the folder
-Just open the files in browser: -index.html → upload page -dashboard.html → results dashboard -No extra installation required — pure HTML, CSS, JavaScript.

#Pages Overview 1️.Upload Page (index.html)

-Choose an Excel file

-Click Upload

-Shows success/error message

-Button to go to dashboard

2️. Dashboard Page (dashboard.html)

-Loads processed file list from backend

-Shows approved/rejected counts

-Allows downloading processed files

-Tech Stack

-HTML5

-CSS3

-Vanilla JavaScript

-Backend required for API communication
