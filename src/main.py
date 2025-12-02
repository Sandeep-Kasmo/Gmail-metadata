import ezgmail
from bs4 import BeautifulSoup as bs
# from config_loader import config
import pandas as pd
from upload import upload
from database import connect
import warnings
from bs4 import MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
def main():
    print('>>Email Service starting....')
    ezgmail.init()
    print('Email configuration success.\n\nPhase-1:Extraction:\nFetching emails..')

    query='in:inbox is:unread'
    threads=ezgmail.search(query)

    if not threads:
        print(f'!!! No emails found for {query}!.Please try again')
        exit(0)
    print(f'Extracted {len(threads)} unread email(s).\nPhase-1 completed.\n\nPhase-2:Transform:\nExtracting the content..')
    df=[]
    for thread in threads:
        for i in thread.messages:
            try:
                sender=i.sender
                sender=sender.replace('"','').replace('<',' ').replace('>','').replace(':','%3A')
                receiver=i.recipient
                subject=i.subject
                # cc=get_header(i,'Cc') if get_header(i,'Cc') else ""
                msg_id=i.id
                raw_body=i.body if i.body else ""
                clean_body=bs(raw_body,'html.parser').get_text() if raw_body else '[No Body found]'
                attachments_url=upload(i)

                df.append({
                    'id':msg_id,
                    'sender':sender,
                    'receiver':receiver,
                    # 'cc':cc,
                    'subject':subject,
                    'body':clean_body,
                    'attachments_url':attachments_url
                })
            except Exception as e:
                print(f"Error processing Email:{e}")
                return None
    print(f'Extracted {len(df[0])} fields from emails.\nPhase-2 completed.\n\nPhase-3:Load:\nInitiating insertion...')
    if df:
        try:
            dataframe = pd.DataFrame(df)
            engine=connect()
            dataframe.to_sql('gmail_metadata_test',engine,if_exists='replace',index=False)
            if engine:
                engine.dispose()
            print(f"Insertion complete. Inserted {len(dataframe)} rows.\nPhase-3 complete")
            print('\nEmail ETL pipeline done...!')
        except Exception as e:
            print(f'Error insertion:{e}')

if __name__=='__main__':
    main()