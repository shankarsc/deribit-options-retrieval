import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import requests
import warnings
warnings.filterwarnings("ignore")

import asyncio
import websockets
import json

def get_instrument(currency, kind):
    """
    Retrieve the latest trades that have occurred for instruments in a specific currency symbol
    in a Pandas DataFrame.

    Parameters
    ----------
    instrument_name - 
    """

    msg =     {
      "jsonrpc" : "2.0",
      "id" : 7617,
      "method" : "public/get_instruments",
      "params" : {
        "currency" : currency,
        "kind" : kind,
        "expired" : False
      }
    }

    async def call_api(msg):
        async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
            await websocket.send(msg)
            while websocket.open:
                response = await websocket.recv()
                return json.loads(response)
                break

    json_dump = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))

    # Cleaning and filtering the dictionary in json_dump
    df = pd.DataFrame(json_dump['result'])['instrument_name']

    return df

