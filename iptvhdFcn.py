import requests

from requests.structures import CaseInsensitiveDict


def iptvhdFcn(url):
    print('iptvhd',url)
    headers = CaseInsensitiveDict()
    r = requests.get(url)
    print(r.status_code)
    a=r.content.decode('latin-1')
    a=a.replace('==','!=',1)
    a=a.split('Clappr.Player(')[1]
    b=a.split('{')[1]
    b=b.split('\'')[1]
    print (b)
    return b
