# HDFC_PROJECT
#Excel File Upload & Loan Processing System (Frontend + Backend)

-This project is a full-stack system that allows users to upload Excel files, automatically processes each row to determine approval or rejection status, and displays results through a clean dashboard interface. The system includes a FastAPI backend that handles file processing and a frontend built with pure HTML, CSS, and JavaScript, making it lightweight and easy to run.

Features
#🔹 Frontend

-Upload Excel files (.xlsx)

-Clean UI with success/error messages

-Dashboard showing:

-Total processed files

-Approved & rejected row counts

-Table listing each processed file

-Download link for processed files

#🔹 Backend

-Accepts Excel uploads via REST API

-Validates file format

-Applies approval logic:

-Approved only if Document Submitted, KYC Submitted, and Business Proof Submitted are all "Yes"

-Generates a processed CSV file with Status column

-Stores processed files with timestamped names

-Returns data for frontend dashboard

-Allows downloading processed results

#Project Structure project/ │── backend/ │ ├── server.py │ ├── requirements.txt │ ├── .env │ └── processed_file/ # auto-generated │ │── frontend/ │ ├── index.html │ ├── dashboard.html │ └── style.css

🔗 API Endpoints (Backend – FastAPI) -Action Method Endpoint -Upload Excel file POST /api/upload -List processed files GET /api/processed-files -Download processed file GET /api/download/{filename} #How It Works 1️.Upload File

-Frontend sends Excel file → Backend validates → Backend saves raw file.

2️. Processing

-Backend reads Excel → checks 3 columns:

-Document Submitted

-KYC Submitted

-Business Proof Submitted

If all are “Yes” → Approved Else → Rejected

3️. Output

-Backend generates:

{original_name}_{timestamp}_processed.csv

Includes:

-All original data

-New "Status" column

4️.Dashboard

-Frontend fetches summary and details using:

-/api/processed-files

-User can click Download to get processed CSV.

#Running the Frontend

-No installation required.

-Just open the two files in browser:

-index.html → Upload

-dashboard.html → View results

-Backend must be running at:

-http://127.0.0.1:8000

#Running the Backend -Install dependencies -pip install -r requirements.txt

-Start the FastAPI server -uvicorn server:app --reload --port 8000

-Environment Variables (.env) MONGO_URL="mongodb://localhost:27017" DB_NAME="test_database" CORS_ORIGINS="*"

#MongoDB is initialized but optional (not required for main Excel processing).

#Expected Excel Format

-Required columns (case-insensitive):

-Document Submitted

-KYC Submitted

-Business Proof Submitted

#Optional: -Backend automatically trims whitespace and handles missing/empty rows.

-Processed Files

-Stored in:

-backend/processed_file/

-Files include:

-Approved count

-Rejected count

#Downloadable processed CSV

#Tech Stack

#Frontend:

-HTML

-CSS

-JavaScript (Fetch API)

#Backend:

-FastAPI

-Python

-pandas

-openpyxl

File-based storage

CORS Enabled
