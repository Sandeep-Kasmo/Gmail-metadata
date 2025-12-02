
# 📧 Gmail ETL Pipeline

This project is a **Gmail Email Metadata ETL Pipeline** that:
1. Extracts unread emails from Gmail  
2. Parses and cleans email content  
3. Uploads attachments to AWS S3  
4. Loads metadata into SQL Server using SQLAlchemy + pyodbc  

---

## 📁 Project Structure
```
gmail-etl/
│
├── attachments/               # temporary folder for downloaded email attachments
│
├── config/
│   └── config.ini             # stores SQL Server + AWS config
│
├── src/
│   ├── main.py                # ETL pipeline (Extract → Transform → Load)
│   ├── upload.py              # S3 upload module
│   ├── database.py            # SQL Server connection engine
│   ├── config_loader.py       # configuration loader
│   └── ...
│
├── credentials.json           # Gmail OAuth credentials (ignored in Git)
├── token.json                 # Gmail OAuth token (ignored in Git)
├── .gitignore
└── README.md
```

---

## ⚙️ Features

### ✔ Extract Phase
- Fetches unread emails from Gmail using `ezgmail`
- Supports Gmail query filtering
- Handles missing bodies/HTML

### ✔ Transform Phase
- Cleans HTML bodies using BeautifulSoup
- Extracts metadata (sender, receiver, subject, body)
- Uploads attachments to S3 and stores URLs
- Converts data into a Pandas DataFrame

### ✔ Load Phase
- Inserts DataFrame into SQL Server (`gmail_metadata_test`)
- Uses SQLAlchemy engine + pyodbc
- Handles connection cleanup

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd gmail-etl
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gmail OAuth
Place your `credentials.json` in the project root.  
A `token.json` will be generated automatically on first run.

---

## 📁 Config File Setup (`config/config.ini`)

```
[sql]
server = YOUR_SERVER_NAME
database = YOUR_DATABASE_NAME
driver = ODBC Driver 17 for SQL Server

[aws]
bucket = your-s3-bucket-name
region = your-aws-region
```

---

## 🚀 Running the ETL Pipeline

```bash
python src/main.py
```

---

## 🧪 Testing
1. Send an email to your Gmail inbox  
2. Add attachments (optional)  
3. Run the pipeline  
4. Validate:
   - Attachments appear in AWS S3  
   - SQL table `gmail_metadata_test` has new rows  
   - Body text is cleaned  

---

## 🛑 Sensitive Files Auto-Ignored via `.gitignore`
- `credentials.json`
- `token.json`
- `/attachments`
- `__pycache__/`
- IDE/OS files

---

## 📦 Requirements
See `requirements.txt`.

---

## 📬 Future Enhancements
- Add CC/BCC extraction  
- Add scheduling (cron, Airflow)  
- Add email notifications after ETL run  

---

Enjoy your **Gmail ETL Pipeline** 🚀
