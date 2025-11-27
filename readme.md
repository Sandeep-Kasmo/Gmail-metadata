📧 Gmail Email Metadata ETL → SQL Server + AWS S3

A lightweight ETL pipeline that extracts email metadata + attachments from Gmail, uploads attachments to S3, and loads all structured data into SQL Server.

📁 Project Structure

   gmail_metadata_etl/
   │── config/
   │     └── config.ini                 # (Ignored in Git – contains secrets)
   │── src/
   │     ├── extract.py                 # Gmail extraction
   │     ├── transform.py               # Data cleaning
   │     ├── load.py                    # S3 upload + DB insert
   │     ├── db.py                      # SQL Server connection + insert
   │     ├── s3_client.py               # AWS S3 uploader
   │     ├── config_reader.py           # INI config loader
   │     └── main.py                    # ETL orchestrator
   │── credentials.json                 # Gmail OAuth credentials (ignored)
   │── token.json                       # Generated automatically (ignored)
   │── requirements.txt
   │── readme.md
   │── temp/
   │── .gitignore

🚀 Features
✔ Gmail Email Extraction

Reads email metadata: From, To, CC, Subject, Body, Date

Downloads attachments (PDF, images, docs, etc.)

Limits to N emails using max_results

✔ AWS S3 Upload

Uploads each attachment as raw bytes

Stores s3://bucket/key URLs in SQL

✔ SQL Server Load

Inserts metadata into Email_Communications

Insert attachment metadata in Email_Attachments

Uses pyodbc and Windows Trusted Authentication

✔ Modular ETL

extract → transform → load pipeline

Config-driven (everything in config.ini)

⚙️ Setup & Installation

1. Clone the repository

   git clone <your-repo-url>
   cd gmail_metadata_etl

3. Install dependencies

   pip install -r requirements.txt

5. Create config.ini (DO NOT COMMIT)

Create this file:

   gmail_metadata_etl/
       config/
           config.ini


Use this template (example):

   [GOOGLE]
   credentials_json = ../credentials.json
   token_json = ../token.json
   gmail_query = is:unread
   
   [AWS]
   bucket_name = your-s3-bucket
   region = ap-south-1
   
   [DATABASE]
   driver = ODBC Driver 17 for SQL Server
   server = YOURPCNAME\SQLSERVER
   database = YourDatabaseName
   trusted_connection = Yes
   
   [GENERAL]
   temp_dir = ../temp

4. Add Gmail OAuth credentials

Download credentials.json from:

👉 https://console.cloud.google.com/apis/credentials

Place it at project root:

   gmail_metadata_etl/credentials.json

5. Run the ETL

From project root:

   python -m src.main


First run will:

Open browser

Ask you to grant Gmail read access

Generate token.json

📤 What the ETL Does (Step-by-Step)

1️⃣ Extract (src/extract.py)

Connects to Gmail using OAuth

Searches emails based on filter (gmail_query)

Fetches metadata + attachments

Decodes Base64 body text

2️⃣ Transform (src/transform.py)

Splits sender name & email

Normalizes fields for DB

Prepares attachment metadata

3️⃣ Load (src/load.py)

Uploads every attachment to S3

Inserts one record per email into Email_Communications

Inserts one record per attachment into Email_Attachments

Commits to SQL Server

🗄 SQL Database Schema

Table: Email_Communications

   Column	Type	Description
   message_id	varchar	Gmail message ID (PK)
   thread_id	varchar	Gmail thread ID
   date_received	varchar	Date header
   sender_name	varchar	Sender name
   sender_email	varchar	Sender email
   receiver_emails	varchar	To header
   cc	varchar	CC header
   subject	varchar	Subject line
   body_text	text	Email body
   attachment_1_url	varchar	First attachment S3 URL
   attachment_2_url	varchar	Second attachment S3 URL
   attachments_json	text	JSON of all attachments
   
Table: Email_Attachments

   message_id
   
   filename
   
   s3_url
   
   mime_type
   
   size_bytes

🔒 Security (Important)

.gitignore already protects:

   credentials.json
   
   token.json
   
   config/config.ini
   
   AWS credentials
   
   temp files

Never push these files to GitHub.

🧪 Testing the ETL

Test extraction only:

   from src.extract import extract_emails
   emails = extract_emails(max_results=5)
   print(emails)


Test DB connection:

   from src.db import establish_conn
   establish_conn()


Test S3 upload:

   from src.s3_client import upload_bytes
   upload_bytes(b"test", "test-folder/test.txt")

🔄 Common Issues

❌ Google OAuth "Access blocked"

→ You must publish the OAuth consent screen or

→ Add your email as Test User

❌ SQL Server connection error

→ Ensure:

SQL Browser running

TCP/IP enabled

Port 1433 open

Server name matches: PCNAME\SQLSERVER

❌ Attachments empty

→ Some emails only contain HTML

→ Extend extractor to parse text/html

📝 License

This project is for internal training, learning, and ETL automation use.
