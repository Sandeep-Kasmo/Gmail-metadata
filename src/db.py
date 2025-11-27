import pyodbc # type: ignore
from config_reader import load_config

cfg = load_config()

server=cfg['DATABASE']['server']
database=cfg['DATABASE']['database']
driver=cfg['DATABASE']['driver']

def establish_conn():
    try:
        conn=pyodbc.connect(f"""
Driver={{{driver}}};
SERVER={server};
DATABASE={database};
Trusted_Connection=Yes;
        """)
        if conn:
            print('connected')
            return conn
    except Exception as e:
        print(f'>>Error conneting to DATABASE:{e}\n')
        return None

def create_tables_if_not_exist(conn):
    # create Email_Communications and Email_Attachments if they don't exist
    sql = """IF OBJECT_ID('dbo.Email_Communications','U') IS NULL
BEGIN
 CREATE TABLE dbo.Email_Communications(
   id BIGINT IDENTITY(1,1) PRIMARY KEY,
   message_id VARCHAR(255) UNIQUE,
   thread_id VARCHAR(255),
   date_received DATETIME,
   sender_name NVARCHAR(255),
   sender_email NVARCHAR(255),
   receiver_emails NVARCHAR(MAX),
   cc NVARCHAR(MAX),
   subject NVARCHAR(MAX),
   body_text NVARCHAR(MAX),
   attachment_1_url NVARCHAR(1024),
   attachment_2_url NVARCHAR(1024),
   attachments_json NVARCHAR(MAX),
   created_at DATETIME DEFAULT GETDATE()
 );
END
IF OBJECT_ID('dbo.Email_Attachments','U') IS NULL
BEGIN
 CREATE TABLE dbo.Email_Attachments(
   id BIGINT IDENTITY(1,1) PRIMARY KEY,
   message_id VARCHAR(255),
   filename NVARCHAR(512),
   s3_url NVARCHAR(1024),
   mime_type NVARCHAR(255),
   size_bytes BIGINT,
   created_at DATETIME DEFAULT GETDATE()
 );
 ALTER TABLE dbo.Email_Attachments
   ADD CONSTRAINT FK_Email FOREIGN KEY(message_id) 
   REFERENCES dbo.Email_Communications(message_id);
END
"""
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        print('>>Error creating tables:', e,'\n')

def insert_email(conn, meta, attachments):
    insert_sql = """INSERT INTO dbo.Email_Communications
    (message_id,thread_id,date_received,sender_name,sender_email,receiver_emails,cc,subject,body_text,attachment_1_url,attachment_2_url,attachments_json)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
    urls = [a.get('s3_url') for a in attachments] if attachments else []
    att1 = urls[0] if len(urls)>0 else None
    att2 = urls[1] if len(urls)>1 else None
    import json
    attachments_json = json.dumps(attachments) if attachments else None
    params = (
        meta.get('message_id'),
        meta.get('thread_id'),
        meta.get('date_received'),
        meta.get('sender_name'),
        meta.get('sender_email'),
        meta.get('receiver_emails'),
        meta.get('cc'),
        meta.get('subject'),
        meta.get('body_text'),
        att1,
        att2,
        attachments_json
    )
    try:
        cur = conn.cursor()
        cur.execute(insert_sql, params)
        # insert attachments
        insert_att = """INSERT INTO dbo.Email_Attachments (message_id, filename, s3_url, mime_type, size_bytes) VALUES (?, ?, ?, ?, ?)"""
        for a in attachments or []:
            cur.execute(insert_att, (meta.get('message_id'), a.get('filename'), a.get('s3_url'), a.get('mime_type'), a.get('size')))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print('>>Insert error:', e,'\n')
        try:
            conn.rollback()
        except:
            pass
        return False
