import requests
import time
import hashlib
import hmac
import re
import json
import click

from requests.api import get
from api import API_KEY, SECRET_KEY

FEE = 0.02

# TODO:
# Add error checking on requests using the status code of the response

def sign_request(api_secret, verb, path, time, body = '') -> str:
    """Signs the request payload using the api key secret"""
    # This is basically boilerplate to interact with VALR's API

    payload = '{}{}{}{}'.format(time,verb.upper(),path,body)
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature

def getData(info: str, curr_pair: str = 'BTCZAR') -> str:
    # Pass as argument. Only need one function for implemented GET endpoints
    getType = {
        'balance': 'https://api.valr.com/v1/account/balances',
        'status': 'https://api.valr.com/v1/public/status',
        'market': {
            'BTCZAR': 'https://api.valr.com/v1/public/BTCZAR/marketsummary',
            'ETHZAR': 'https://api.valr.com/v1/public/ETHZAR/marketsummary',
            'XRPZAR': 'https://api.valr.com/v1/public/XRPZAR/marketsummary'
        }
    }

    # Use currency pair argument if needed for market data
    url = getType['market'][curr_pair] if 'market' in info else getType[info]

    payload = {}
    headers ={
        'X-VALR-API-KEY': API_KEY,
        'X-VALR-SIGNATURE': sign_request(SECRET_KEY, 'get', re.findall('/v1.*', url)[0], int(time.time()*1000)),
        'X-VALR-TIMESTAMP': str(int(time.time()*1000))
    }

    response = requests.request('GET', url, headers=headers, data=payload)
 
    return response.text

@click.group()
def valr():
    """A CLI for interacting with the VALR exchange"""

@click.option('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def market_data(pair: str):
    print(getData('market', pair))

@click.option('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def history_pair():
    print('Not Implemented')

@click.option('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def quote():
    print('Not Implemented')

@click.option('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def order():
    print('Not Implemented')

@valr.command()
def history():
    print('Not Implemented')

@valr.command()
def status():
    print(getData('status'))

@valr.command()
def balance():
    balance_info = json.loads(getData('balance'))
    for currencies in balance_info:
        if currencies['available'] != '0':
            print(f'You have {currencies["available"]} {currencies["currency"]}') 

def main():
    valr(prog_name='valr')

if __name__ == "__main__":
    main()