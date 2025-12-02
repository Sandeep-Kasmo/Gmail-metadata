import boto3
import os
from config_loader import config
bucket=config['aws']['bucket']
temp_dir='attachments'

def upload(message):

    if not message.attachments:
        return "No attachments"
    message.downloadAllAttachments(downloadFolder=temp_dir)
    s3_client=boto3.client('s3')

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    s3_urls=[]

    try:
        for filename in message.attachments:
            local_path=os.path.join(temp_dir,filename)
            s3_key=f"attachments/{filename}"
            s3_client.upload_file(local_path,bucket,s3_key)
            s3_urls.append(f"s3://{bucket}/{s3_key}")

            if os.path.exists(local_path):
                # pass
                os.remove(local_path)
        return ", ".join(s3_urls)
    except Exception as e:
        print(f"Error uploading file:{e}")
        return "Error"
