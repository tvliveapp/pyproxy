import requests

from requests.structures import CaseInsensitiveDict
import json
'''
http://iptvhd.club/aptv/vip/cablehd.php?id=2_
http://aptv.radiotormentamx.com/aptv/vip/cablehd.php?id='+fid+'_#
'''

channels={}
url="https://raw.githubusercontent.com/tvliveapp/channels/master/aptv.json"
def updateChns():
    global channels
    resp = requests.get(url)
    print(resp.status_code)
    channels = json.loads(resp.text)
    return resp.status_code
updateChns()    

def iptvhdFcn(id):
    print('id',id,channels[id]["srclink"])
    if channels[id]["srclink"]== "iptvhd":
        headers = CaseInsensitiveDict()
        r = requests.get(channels[id]['stream_link'])
        print(r.status_code)
        a=r.content.decode('latin-1')
        a=a.replace('==','!=',1)
        a=a.split('Clappr.Player(')[1]
        b=a.split('{')[1]
        b=b.split('\'')[1]
        print (b)
        return b
    else:
        return channels[id]['stream_link']
    
print(iptvhdFcn('aptv11'))
