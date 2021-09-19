import asyncio
import websockets
import json
import nest_asyncio
nest_asyncio.apply()

import pandas as pd

def ticker(instrument_name):
    """
    Retrieve the latest trades that have occurred for instruments in a specific currency symbol
    in a Pandas DataFrame.

    Parameters
    ----------
    instrument_name - 
    """

    # Message for API request
    msg = \
        {
        "jsonrpc" : "2.0",
        "id" : 8772,
        "method" : "public/ticker",
        "params" : {
            "instrument_name" : instrument_name,
            }
    }

    # Function call for API request
    async def call_api(msg):
        async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
            await websocket.send(msg)
            while websocket.open:
                response = await websocket.recv()
                return json.loads(response)
                break

    json_dump = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))

    # Cleaning and filtering the dictionary in json_dump
    result_dump = dict((i, json_dump[i]) for i in ['result'])
    df = pd.DataFrame.from_dict(result_dump).T
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df
