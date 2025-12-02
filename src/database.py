import sqlalchemy
from config_loader import config
from sqlalchemy import create_engine
import urllib

SERVER=config['sql']['server']
DRIVER=config['sql']['driver']
DATABASE=config['sql']['database']

def connect():
    params=urllib.parse.quote_plus(f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=Yes")
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    # print('connected')
    return engine

# connect()