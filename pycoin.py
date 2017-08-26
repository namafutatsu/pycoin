#!/usr/bin/env python3

from urllib.parse import urljoin, urlencode
import sys

import requests

BASE_URL = 'https://mobile.leboncoin.fr'

LBC_APP_ID = 'leboncoin_android'
LBC_APP_KEY = 'd2c84cdd525dddd7cbcc0d0a86609982c2c59e22eb01ee4202245b7b187f49f1546e5f027d48b8d130d9aa918b29e991c029f732f4f8930fc56dbea67c5118ce'

LBC_PARAMS = {
    'app_id': LBC_APP_ID,
    'key': LBC_APP_KEY,
    'ca': '12_s',
    'w': '1',
    'f': 'a',
    'o': '1',
    'sp': 0,
    'pivot': '0,0,0',
}


def cast_price(p):
    try:
        return int(p.strip().replace(' ', ''))
    except ValueError:
        return 0


class LbcAd:
    def __init__(self, url, list_id, list_time, category_id, subject, region, dpt_code, zipcode, city, price, **kwargs):
        self.url = url
        self.list_id = list_id
        self.list_time = list_time
        self.price = cast_price(price)
        self.category_id = category_id
        self.subject = subject
        self.region = region
        self.dpt_code = dpt_code
        self.zipcode = zipcode
        self.city = city

    def __str__(self):
        return '{s.list_time} {s.price} {s.subject} {s.city} {s.url}'.format(s=self)


class LbcResponse:
    def __init__(self, total, lastpagenumber, ads=None, numperpage=20, **kwargs):
        self.total = total
        self.numperpage = numperpage
        self.lastpagenumber = lastpagenumber
        if ads is not None:
            self.ads = [LbcAd(**x) for x in ads]


def list_items(query):
    params = LBC_PARAMS.copy()
    params.update({'q': query})
    url = urljoin(BASE_URL, 'templates/api/list.json') + '?' + urlencode(params)
    ret = requests.post(url)
    ret.raise_for_status()

    lbc_response = LbcResponse(**ret.json())
    print('Found {total} responses.'.format(total=lbc_response.total))
    for ad in lbc_response.ads:
        print(ad)


list_items(sys.argv[1])
