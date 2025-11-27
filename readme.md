Simple Gmail → S3 → SQL Server ETL

How to run:
1. Put your Google credentials.json one level above src or update config.ini path.
2. Fill config/config.ini with your AWS bucket and SQL Server details.
3. Install requirements:
   pip install -r requirements.txt
4. Run:
   python -m src.main

Notes:
- This project uses Trusted Connection for SQL Server via pyodbc. If you need username/password, modify src/db.py.
- AWS credentials must be available to boto3 (env vars or instance role).
