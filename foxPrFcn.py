import requests
import json
import base64
#from pyaes import aes
from requests.structures import CaseInsensitiveDict
#"fs1ar"  "fs2ar" "fs3ar" "fspar"
url1="https://cdn.tsnt.xyz/"
url2=".json"
passw='.3tnt99'

def foxPrFcn(url):
    print('fox',url)
    headers = CaseInsensitiveDict()
    resp = requests.get(url1+url+url2)
    print(resp.text)
    urlStr=json.loads(resp.text)
    print(urlStr["source"])
    base64_bytes = urlStr["source"].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    print(message)
    return message
def tntSp():
    url='https://sv.televisionlibre.net/json/tntsports.json'
    print('tnt',url)
    headers = CaseInsensitiveDict()
    resp = requests.get(url)
    print(resp.text)
    urlStr=json.loads(resp.text)
    print(urlStr["token"])
    
    message = urlStr["token"]
    print(type(message))
    #print(aes.decrypt(urlStr['token'],passw))
    return message
#foxPrFcn("fspar")
#tntSp()
