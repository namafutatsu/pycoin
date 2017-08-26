import math


def lbc_cast_int(p):
    try:
        return int(p.strip().replace(' ', ''))
    except ValueError:
        return 0


class LbcAd:
    def __init__(self, url, list_id, list_time, category_name, category_id, subject, region, dpt_code, zipcode, city, price, **kwargs):
        self.url = url
        self.list_id = list_id
        self.list_time = list_time
        self.price = lbc_cast_int(price)
        self.category_name = category_name
        self.category_id = category_id
        self.subject = subject
        self.region = region
        self.dpt_code = dpt_code
        self.zipcode = zipcode
        self.city = city

    def __str__(self):
        return '{s.list_time} {s.price} {s.subject} {s.city} {s.category_id} {s.category_name} {s.url}'.format(s=self)

    def category_within(self, categories):
        return self.category_id in categories

    def department_within(self, departments):
        return self.dpt_code in departments

    def price_within(self, price_min=0, price_max=math.inf):
        return self.price > price_min and self.price < price_max


class LbcResponse:
    def __init__(self, total, paging_last, lastpagenumber, ads=None, numperpage=20, **kwargs):
        self.total = int(total)
        self.numperpage = int(numperpage)
        self.lastpagenumber = lbc_cast_int(lastpagenumber)
        self.paging_last = paging_last
        if ads is not None:
            self.ads = [LbcAd(**x) for x in ads]
