import boto3 # type: ignore
from config_reader import load_config
cfg = load_config()
_bucket = cfg['AWS']['bucket_name']
_region = cfg['AWS'].get('region', 'us-east-1')
_s3 = boto3.client('s3', region_name=_region)

def upload_bytes(data_bytes, key):
    if data_bytes is None:
        raise ValueError('No data to upload')
    _s3.put_object(Bucket=_bucket, Key=key, Body=data_bytes)
    return f's3://{_bucket}/{key}'

