import requests
import time
import hashlib
import hmac
import re
import json
import click

from api import API_KEY, SECRET_KEY

FEE = 0.02

# TODO:
# Add error checking on requests using the status code of the response

response = ''

def sign_request(api_secret, verb, path, time, body = '') -> str:
    """Signs the request payload using the api key secret"""
    # This is basically boilerplate to interact with VALR's API

    payload = '{}{}{}{}'.format(time,verb.upper(),path,body)
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature

def getData(info: str, curr_pair) -> str:
    # Pass as argument. Only need one function for implemented GET endpoints
    getType = {
        'balance': 'https://api.valr.com/v1/account/balances',
        'status': 'https://api.valr.com/v1/public/status',
        'market': 'https://api.valr.com/v1/public/*/marketsummary',
    }

    url = getType[info]

    if re.search('/\*/', url) == True:
        pass
        #We want to replace /*/ with the currency pair the user gives directly if market is arg

    payload = {}
    headers ={
        'X-VALR-API-KEY': API_KEY,
        'X-VALR-SIGNATURE': sign_request(SECRET_KEY, 'get', re.findall('/v1.*', url)[0], int(time.time()*1000)),
        'X-VALR-TIMETAMP': str(int(time.time()*1000))
    }

    response = requests.request('GET', url, headers=headers, data=payload)

    # Checking if API response is good
    if response.status_code == '200':
        return response.json
    else:
        return 'Incorrect'

@click.group()
def valr():
    """A CLI for interacting with the VALR exchange"""

@click.argument('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def market_data(pair: str):
    print(getData('market', pair))

@click.argument('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def history_pair():
    print('Not Implemented')

@click.argument('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
@valr.command()
def quote():
    print('Not Implemented')

@click.argument('-p', '--pair', help='Currency Pair used for command\nexample: BTCZAR, ETHZAR')
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