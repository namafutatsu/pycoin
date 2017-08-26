#!/usr/bin/env python3

import argparse
import math

import pycoin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', help='LBC application ID')
    parser.add_argument('--app-key', help='LBC application key')

    parser.add_argument('--price-min', type=int, default=0, help='minimum price')
    parser.add_argument('--price-max', type=int, default=math.inf, help='maximum price')

    parser.add_argument('--categories', nargs='+', help='space-separated whitelist of categories')
    parser.add_argument('--departments', nargs='+', help='space-separated whitelist of departments')

    parser.add_argument('query', help='the search query text')
    args = parser.parse_args()

    client = pycoin.Client(args.app_id, args.app_key)

    n = client.count_ads(args.query)
    print("{} ads found.".format(n))

    for ad in client.list_ads(
            args.query,
            sort=pycoin.BY_PRICE,
            price_min=args.price_min,
            price_max=args.price_max,
            categories=args.categories,
            departments=args.departments):
        print(ad)


if __name__ == '__main__':
    main()
