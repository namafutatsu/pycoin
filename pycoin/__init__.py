import math
from urllib.parse import urljoin, urlencode

import requests

from .models import LbcResponse

BASE_URL = 'https://mobile.leboncoin.fr'

BY_DATE = 0
BY_PRICE = 1

REGION_IDF = 12

CATEGORY_VOITURES = '2'
CATEGORY_CARAVANING = '4'
CATEGORY_VENTES_IMMO = '9'
CATEGORY_LOCATIONS = '10'
CATEGORY_COLOCATIONS = '11'
CATEGORY_VETEMENTS = '22'


class Client:
    def __init__(self, app_id, app_key, region=REGION_IDF):
        self.app_id = app_id
        self.app_key = app_key
        self.region = region

    def api_params(self):
        return {
            'app_id': self.app_id,
            'key': self.app_key,
            'ca': '{}_s'.format(self.region),
            'w': '0',  # "zoom" level. 1 = the region, 2 = whole country. 275 = Paris, 293 = Seine Saint-Denis, ...
            'f': 'a',  # still unknown.
            'sp': 0,  # sort by: 0 = date, 1 = price
            'o': '1',  # page number
            'pivot': '0,0,0',  # API pagination cursor
        }

    def _api_post(self, **extra_params):
        params = self.api_params()
        params.update(extra_params)
        url = urljoin(BASE_URL, 'templates/api/list.json') + '?' + urlencode(params)
        ret = requests.post(url)
        ret.raise_for_status()
        return ret.json()

    def count_ads(self, query):
        return self._api_post(q=query)['total']

    def list_ads(self, query, sort=BY_DATE, price_min=0, price_max=math.inf, departments=None, categories=None):
        data = self._api_post(q=query, sp=str(sort))
        lbc_response = LbcResponse(**data)
        for ad in lbc_response.ads:
            if ad.price_within(price_min, price_max) and ad.department_within(departments) and ad.category_within(categories):
                yield ad
        for i in range(2, lbc_response.lastpagenumber):
            data = self._api_post(q=query, sp=str(sort), pivot=lbc_response.paging_last, o=i)
            lbc_response = LbcResponse(**data)
            for ad in lbc_response.ads:
                if ad.price_within(price_min, price_max) and ad.department_within(departments) and ad.category_within(categories):
                    yield ad
