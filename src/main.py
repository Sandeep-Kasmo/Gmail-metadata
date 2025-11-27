from extract import extract_emails
from transform import transform
from load import load

def run_etl():
    print('ETL Start')
    raw = extract_emails()
    if not raw:
        print('No messages found.')
        return
    clean = transform(raw)
    load(clean)
    print('ETL Done')

if __name__ == '__main__':
    run_etl()
