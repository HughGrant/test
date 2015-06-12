import requests
import time
import json


def get_ibt_cost(country_id, weight):
    url = '''
        http://183.62.161.176/custcenter/calculate!calculate.action?
        callback=&vo.packageType=2&vo.tempIds=0&vo.textileInd=N&
        vo.dbatteryInd=N&vo.dbatteryableInd=N&vo.pbatteryInd=N&
        vo.ybatteryInd=N&vo.cellphoneInd=N&vo.cbatteryInd=N&
        vo.poboxaddrInd=N&vo.telInd=Y&vo.oriInvoice=N&
        vo.longweightInd=N&vo.homeaddrInd=N&
        vo.tradedeclareInd=N&vo.countryId={0}&vo.packageQty=1&
        vo.packageWeight={1}&vo.declarePrice=0&vo.recZipcode=&vo.recCity=&
        vo.vstring={2}%2C0%3B&_={3}'''
    ms = int(time.time())
    url = url.format(country_id, weight, weight, ms)
    url = url.replace(' ', '').replace('\n', '').strip()
    r = requests.get(url)
    c = json.loads(r.text[1:-2])
    print(c)
