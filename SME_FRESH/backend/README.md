#To run: uvicorn server:app --reload --host 0.0.0.0 --port 8000
# Loan Approval System - Backend API

A FastAPI backend service that processes loan application files and determines approval status based on document submission criteria.

## Features

- Upload Excel (.xlsx, .xls) files containing loan applications
- Automatic approval/rejection based on document submission status
- Download processed CSV files with approval status
- List all processed files with metadata

## Approval Logic

A loan application is **Approved** if and only if ALL three conditions are met:
1. Income Document Submitted = "Yes"
2. KYC Submitted = "Yes"
3. Business Proof Submitted = "Yes"

If any of the above conditions is not met, the application is **Rejected**.

## API Endpoints

### 1. Upload and Process Loan File
**POST** `/api/upload`

Uploads an Excel file containing loan applications and returns a processed CSV with approval status.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (Excel file)

**Response:**
- Returns a CSV file with an additional "Status" column (Approved/Rejected)
- File is automatically downloaded with naming format: `{original_filename}_{timestamp}_processed.csv`

**Example using curl:**
```bash
curl -X POST "https://quick-chat-backend.preview.emergentagent.com/api/upload" \
  -F "file=@your_loan_file.xlsx" \
  -o result.csv
```

### 2. List Processed Files
**GET** `/api/processed-files`

Returns a list of all processed CSV files with metadata.

**Response:**
```json
{
  "total_files": 1,
  "files": [
    {
      "filename": "loan_file_20251205_071756_processed.csv",
      "size_bytes": 14832,
      "created_at": "2025-12-05T07:17:56.906787+00:00",
      "download_url": "/api/download/loan_file_20251205_071756_processed.csv"
    }
  ]
}
```

**Example using curl:**
```bash
curl "https://quick-chat-backend.preview.emergentagent.com/api/processed-files"
```

### 3. Download Processed File
**GET** `/api/download/{filename}`

Downloads a specific processed CSV file.

**Example using curl:**
```bash
curl "https://quick-chat-backend.preview.emergentagent.com/api/download/loan_file_20251205_071756_processed.csv" \
  -o downloaded_file.csv
```

## File Storage

All uploaded Excel files and processed CSV files are stored in:
```
/app/backend/processed_file/
```

Files are named with timestamps to prevent conflicts:
- Uploaded: `{original_name}_{timestamp}.xlsx`
- Processed: `{original_name}_{timestamp}_processed.csv`

## Expected Excel File Format

The Excel file should contain the following columns (column names are case-insensitive):
- Applicant ID
- Applicant's Industry
- Loan Amount Requested
- Loan Category
- Applicant's Category
- Income Document Submitted (Yes/No)
- KYC Submitted (Yes/No)
- Business Proof Submitted (Yes/No)

**Note:** The system can handle Excel files where headers are in the first row or second row.

## Technical Details

- **Framework:** FastAPI
- **Excel Processing:** pandas + openpyxl
- **Storage:** File system (processed_file directory)
- **CORS:** Enabled for all origins
- **Port:** 8001 (internal)

## Error Handling

The API provides clear error messages for:
- Invalid file formats (non-Excel files)
- Missing required columns
- Empty files
- File processing errors

## Installation

Required Python packages:
```bash
pip install fastapi uvicorn pandas openpyxl python-multipart
```

## Running the Server

The server runs automatically via supervisor:
```bash
sudo supervisorctl restart backend
```

## Logs

Backend logs are available at:
```bash
tail -f /var/log/supervisor/backend.*.log
```
