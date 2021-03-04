import os
import requests
from requests.structures import CaseInsensitiveDict

from lxml import html

from flask import request
from flask import Flask
from flask import Response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'





@app.route('/')
def home():
    usage = 'Pass a properly encoded url parameter e.g. /https/www.google.com'
    return usage

@app.route('/iptvhd/<id>')
@cross_origin()
def iptvhd(id):
    url = "http://iptvhd.club/aptv/vip/cablehd.php?id="
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "loaB6oIZOla892u1q9qoi9j31BrzLRzQgfTrvXYGnfIVrkwb9402QA44LkyZf98xmMznUTqpoIZoeQk"
    headers["Referer"] = ""
    resp = requests.get(url, headers=headers)
    a=resp.text.split('Clappr.Player(')[1]
    b=a.split('{')[1]
    return(b.split('\'')[1])

import base64
@app.route('/https/<url>')
@cross_origin()
def root(url):    
    
    print("base64 url>>>",url)
    url=base64.b64decode(url).decode("UTF-8") 
    print("url>>>",url)
    r = requests.get(url)
   
    rr = Response(response=r.content, status=r.status_code)
    #rr = Response(response=b, status=r.status_code)
    
    print(r.headers['Content-Type'])
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

@app.route('/ref/<url>')
def ref(url):    
    
    print("base64 url>>>",url)
    url=base64.b64decode(url).decode("UTF-8") 
    
    print("url>>>",url)
    headers = CaseInsensitiveDict()
    ref=url.split("|")[1]
    url=url.split("|")[0]
    
    print("ref: "+ref)
    headers["Referer"] =ref
    r = requests.get(url,headers=headers)
    a=r.content.decode('latin-1')
    a=a.replace('==','!=',1)
    a=a.split('Clappr.Player(')[1]
    b=a.split('{')[1]
    b=split('\'')[1]
    rr = Response(response=bytes(b,'utf-8'), status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr
@app.route('/g/<keyword>')
def gkeyword(keyword):    
    url = 'https://www.google.com/search'
    payload = {'q':keyword, 'num':1, 'start':1, 'sourceid':'chrome', 'ie':'UTF-8', 'cr':'cr=countryUS'}
    r = requests.get(url, params=payload)
    rr = Response(response=r.content, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

@app.route('/r/<subreddit>/subscribers')
def gsubreddit(subreddit):
    url = 'https://old.reddit.com/r/' + subreddit
    xpath ="//span[@class='subscribers']/span[@class='number']/text()"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    tree = html.fromstring(r.content)
    subscribers = tree.xpath(xpath)
    rr = Response(response=subscribers, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
