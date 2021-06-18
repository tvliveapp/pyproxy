'''

import os
import requests

from requests.structures import CaseInsensitiveDict

from lxml import html

from flask import request
from flask import Flask
from flask import Response
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

channels={}
url="https://raw.githubusercontent.com/tvliveapp/channels/master/channelsUrl.json"
def updateChns():
    global channels
    resp = requests.get(url)
    channels = json.loads(resp.text)
    return r.status_code
updateChns()    

@app.route('/')
@cross_origin()
def home():
    global channels
    fnc = request.args.get('fnc', default = '', type = str)
    ch = request.args.get('ch', default = 'test', type = str)
    web= request.args.get('web', default = False, type = bool)
    return fnc+' '+ch+' '+str(web)+'\n\n\n\n'+json.dumps(channels)

@app.route('/update/')
@cross_origin()
def update():
    return updateChns()



@app.route('/')
def home():
    page = request.args.get('page', default = 1, type = int)
    filter = request.args.get('filter', default = '*', type = str)
    usage = 'Pass a properly encoded url parameter e.g. /https/www.google.com'+filter
    return usage

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

@app.route('/playlist/<url>')
def playlist(url):
    rr = Response(response=bytes("http://38.18.238.35:2095/102estrellas/transco1/chunk_Auth=ix08x%C2%A0Z6Q7r567Z5%5E@9WxF%C2%A0g7x%C2%A6c=1/playlist.m3u8",'utf-8'), status=200)
    rr.headers["Content-Type"]='text/html'
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
    b=b.split('\'')[1]
    rr = Response(response=bytes(b,'utf-8'), status=r.status_code)
    rr.headers["Content-Type"]="application/vnd.apple.mpegurl"
    return rr

@app.route('/iptvhd/<url>')
def iptvhd(url):    
    
    print("base64 url>>>",url)
    url=base64.b64decode(url).decode("UTF-8") 
    
    print("url>>>",url)
    headers = CaseInsensitiveDict()
    ref=url.split("|")[1]
    vlc=url.split("|")[2]
    url=url.split("|")[0]
    
    print("ref: "+ref)
    headers["Referer"] =ref
    r = requests.get(url,headers=headers)  
    a=r.content.decode('latin-1')
    a=a.replace('==','!=',1)
    a=a.split('Clappr.Player(')[1]
    b=a.split('{')[1]
    b=b.split('\'')[1]
    rr = Response(response=bytes(b,'utf-8'), status=r.status_code)
        
    if vlc=='vlc':
        rr.headers["Content-Type"] = r.headers['Content-Type']
    else:
        rr.headers["Content-Type"]="application/vnd.apple.mpegurl"
    return rr
@app.route('/same/<url>')
def same(url):    
    
    print("base64 url>>>",url)
    url=base64.b64decode(url).decode("UTF-8") 
    
    print("url>>>",url)
    headers = CaseInsensitiveDict()
    ref=url.split("|")[1]
    vlc=url.split("|")[2]
    url=url.split("|")[0]
    
    print("ref: "+ref)
    headers["Referer"] =ref
    r = requests.get(url,headers=headers)
    rr = Response(response=bytes(url,'utf-8'), status=r.status_code)        
    if vlc=='vlc':
        rr.headers["Content-Type"] = 'text/html'
    else:
        rr.headers["Content-Type"]="application/vnd.apple.mpegurl"
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
'''


import os
import requests
import m3u8
from requests.structures import CaseInsensitiveDict

#from lxml import html

from flask import request
from flask import Flask
from flask import Response
from flask_cors import CORS, cross_origin
import json
import iptvhdFcn
import foxPrFcn
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
 
channels={}
ipList=[]
url="https://raw.githubusercontent.com/tvliveapp/channels/master/estaticos.json"
def updateChns():
    global channels, ips
    iptvhdFcn.updateChns()
    resp = requests.get(url)
    print(resp.status_code)
    channels = json.loads(resp.text)
    return resp.status_code
updateChns()
def loadM3u8(url):
    playlist = m3u8.load(url)
    for i in range(len(playlist.segments)):
        playlist.segments[i].uri=playlist.segments[i].absolute_uri
    return playlist.dumps()

@app.route('/')
@cross_origin()
def home():
    global channels, ips
    ip_address = request.headers['X-Forwarded-For']
    if ip_address not in ipList:
        ipList.append(ip_address)
    fnc = request.args.get('fnc', default = '', type = str)
    ch = request.args.get('ch', default = 'test', type = str)
    web= request.args.get('web', default = False, type = bool)
    cType= request.args.get('type', default = 'application/x-mpegURL', type = str)
    prxy=type= request.args.get('type', default =false, type = bool)
    
    rp=''
    if fnc=='iptvhd':
        if proxy:
            rp=loadM3u8(iptvhdFcn.iptvhdFcn(ch))
        else:
            rp=iptvhdFcn.iptvhdFcn(ch) 
    elif fnc=='foxPrFcn':
        rp=foxPrFcn.foxPrFcn(channels[ch]['stream_link'])
    elif fnc=='proxy':
        playlist = m3u8.load('http://iptvhd.club:8081/televall2021/2_.m3u8?token=OYM0xDCO9_amY92fhtwdyw&expires=1619593289')
        for i in range(len(playlist.segments)):
            playlist.segments[i].uri=playlist.segments[i].absolute_uri
        rp=playlist.dumps()
    else:
        if proxy:
            rp=loadM3u8(channels[ch]['stream_link'])
        else:
            rp=channels[ch]['stream_link']
    rr = Response(response=bytes(rp,'utf-8'), status=200)
    rr.headers["Content-Type"] = cType
    '''
    if not web:
        #rr.headers["Content-Type"] = 'text/html'
        rr.headers["Content-Type"] = 'application/x-mpegURL'
    else:
        rr.headers["Content-Type"]="application/vnd.apple.mpegurl"
        rr.headers["Content-Type"] = 'application/x-mpegURL'
    '''
    return rr
@app.route('/update/')
@cross_origin()
def update():
    return str(updateChns(),channels)
@app.route('/ips/')
@cross_origin()
def ips():
    global ipList
    return str(ipList)
 
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
