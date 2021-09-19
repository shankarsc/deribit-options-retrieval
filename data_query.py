import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import get_ticker
import get_instruments
import requests
import warnings
warnings.filterwarnings("ignore")

def ticker_api_query(instrument_name):

    raw_data = pd.DataFrame()

    for i in instrument_name:
        df = get_ticker.ticker(i)
        raw_data = raw_data.append(df)
        # raw_data.insert(0, 'timestamp', str(dt.datetime.now())[0:16])
        print(i, "retrieved...")

    print('Completed API query...')
    
    return raw_data


def data_transform(instrument_name):
    
    data_df = ticker_api_query(instrument_name)
    
    trans_df = data_df[['timestamp', 'instrument_name', 'mark_iv', 'ask_iv', 'bid_iv', 'underlying_price', 'mark_price', 'open_interest', 'interest_rate']]
    trans_df.reset_index(drop=True, inplace=True)
    trans_df['strike_price'] = trans_df['instrument_name']

    greeks = pd.json_normalize(data_df['greeks'])
    trans_df = pd.concat([trans_df, greeks], axis=1)

    for row in range(len(trans_df['instrument_name'])):
        str_start = trans_df['instrument_name'][row].find('-',4)
        str_end = trans_df['instrument_name'][row].find('-',12)
        trans_df['strike_price'][row] = trans_df['instrument_name'][row][str_start:str_end].strip('-')

    trans_df['strike_price'] = pd.to_numeric(trans_df['strike_price'])
    trans_df['delta'] = pd.to_numeric(trans_df['delta'])

    print('Completed data transformation...')
    
    return trans_df

instruments = get_instruments.get_instrument("BTC", "option").sort_values().reset_index(drop=True)
all_options = data_transform(instruments)
all_options['timestamp'] = pd.to_datetime(all_options['timestamp'], unit='ms')

all_options.to_csv(os.getcwd()+"/BTC_options_dataset_{}.csv".format(str(dt.datetime.now())[:16]))
print('Completed CSV extract as /BTC_options_dataset_{}.csv...'.format(str(dt.datetime.now())[:16]))
