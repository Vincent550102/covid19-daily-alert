import requests,json

def crawler():
    return json.loads(requests.get('https://covid19dashboard.cdc.gov.tw/dash3').text)['0']['昨日確診']