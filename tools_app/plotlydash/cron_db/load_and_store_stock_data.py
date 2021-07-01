from datetime import timedelta, datetime
from typing import List
import itertools
import bt
import pandas as pd
from sqlalchemy.orm import Session
from tqdm import tqdm
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from models.close_data import CloseData
from models.session_context import db_session

TICKER_LIST = 'datafiles/tickerlist.csv'


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def create_close_data_objects(row):
    date = row['date']
    return [CloseData(symbol=index, close=value, date=date) for index, value in row.items() if index != 'date']


def get_and_insert_historical_data(tickers: List[str], db: Session, chunk_size):
    chunked_fetch = chunks(tickers, chunk_size)
    now = datetime.now().replace(hour=0, minute=0)
    for chunk in chunked_fetch:
        no_dash_chunk = list(chunk) #The no dash is necessary because we check if btc-usd is in the database, then its not, and then when we go fetch the data 
                                    # we are returned a dataframe of btcusd, and then that is put into the DB but it throws an error because it is already there. 
        
        for i in range(len(no_dash_chunk)):
            if '-' in no_dash_chunk[i]:
                no_dash_chunk[i] = no_dash_chunk[i].replace("-", '')
        multihistories = CloseData.get_multiple_histories(no_dash_chunk, db)
        start = '2017-01-01'
        start_f = datetime(2017, 1, 1, 0, 0)
        if multihistories:
            multihistories.sort(key=lambda x: x.date)
            start_f = multihistories[-1].date + timedelta(days=1)
            start = start_f.strftime("%Y-%m-%d")
            
            
        start_f = datetime(start_f.year, start_f.month, start_f.day, 0, 0) 
        
        #print(start_f, "<", now)
        if start_f < now:
            for _ in range(chunk_size): #loop through all tickers 
                try:
                    fetched_tickers = bt.get(chunk, start=start)
                    print("Fetched:", chunk)
                    fetched_tickers['date'] = fetched_tickers.index
                    close_data = fetched_tickers.apply(create_close_data_objects, axis=1)
                    close_data = list(itertools.chain(*close_data))
                    db.bulk_save_objects(close_data)
                    db.commit()
                    break
                except Exception as e:
                    error = str(e).split()
                    if error[0] == 'No': #If there is a specific ticker that yahoo finance does not have
                        bad_ticker = error[5]
                        print("BAD TICKER", bad_ticker)
                        chunk.remove(bad_ticker)
            
        


with db_session() as db:
    tickers = pd.read_csv(TICKER_LIST)['Ticker']
    tickers.dropna(inplace=True)
    get_and_insert_historical_data(tickers.tolist(), db, 10)
    tickers = pd.read_csv(TICKER_LIST)['ETF']
    tickers.dropna(inplace=True)
    get_and_insert_historical_data(tickers.tolist(), db, 10)
    tickers = pd.read_csv(TICKER_LIST)['Cryptos']
    tickers.dropna(inplace=True)
    get_and_insert_historical_data(tickers.tolist(), db, 2)
