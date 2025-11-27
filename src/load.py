from s3_client import upload_bytes
from db import establish_conn, create_tables_if_not_exist, insert_email

def load(emails):
    conn = establish_conn()
    if not conn:
        raise RuntimeError('DB connection failed')
    create_tables_if_not_exist(conn)
    for e in emails:
        attachments_info = []
        for p in e.get('attachments', []):
            data = p.get('data_bytes')
            if not data:
                continue
            fname = p.get('filename') or 'attachment'
            key = f'email_attachments/{e["message_id"]}/{fname}'
            try:
                s3_url = upload_bytes(data, key)
                attachments_info.append({
                    'filename': fname,
                    's3_url': s3_url,
                    'mime_type': p.get('mimeType'),
                    'size': len(data)
                })
                print('>Uploaded', fname)
            except Exception as ex:
                print('Upload failed for', fname, ex)
        meta = {
            'message_id': e.get('message_id'),
            'thread_id': e.get('thread_id'),
            'date_received': e.get('date_received'),
            'sender_name': e.get('sender_name'),
            'sender_email': e.get('sender_email'),
            'receiver_emails': e.get('receiver_emails'),
            'cc': e.get('cc'),
            'subject': e.get('subject'),
            'body_text': e.get('body_text')
        }
        ok = insert_email(conn, meta, attachments_info)
        print('Inserted' if ok else 'Failed', e.get('message_id'))
    conn.close()
