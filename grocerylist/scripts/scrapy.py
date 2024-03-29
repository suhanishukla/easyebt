# -*- coding: utf-8 -*-
"""scrapy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m_s_y7f6MvBVDlUKWdffsN_gtzHPKS-N
"""

import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from tabulate import tabulate


def create_walmart_product_url(product):
    return 'https://www.walmart.com' + product.get('canonicalUrl', '').split('?')[0]

headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"}
product_url_list = []

## Walmart Search Keyword
keyword = 'ebt eligible'

## Loop Through Walmart Pages Until No More Products
for page in range(1, 5):
    try:
        payload = {'q': keyword, 'sort': 'best_seller', 'page': page, 'affinityOverride': 'default'}
        walmart_search_url = 'https://www.walmart.com/search?' + urlencode(payload)
        response = requests.get(walmart_search_url, headers=headers)

        if response.status_code == 200:
            html_response = response.text
            soup = BeautifulSoup(html_response, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if script_tag is not None:
                json_blob = json.loads(script_tag.get_text())
                product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
                product_urls = [create_walmart_product_url(product) for product in product_list]
                product_url_list.extend(product_urls)
                if len(product_urls) == 0:
                    break

    except Exception as e:
        print('Error', e)


#print(product_url_list)

product_data_list = []

## Loop Through Walmart Product URL List
for url in product_url_list:
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html_response = response.text
            soup = BeautifulSoup(html_response, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if script_tag is not None:
                json_blob = json.loads(script_tag.get_text())
                raw_product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
                product_data_list.append({
                    #'id':  raw_product_data.get('id'),
                    'type':  raw_product_data.get('type'),
                    'name':  raw_product_data.get('name'),
                    'brand':  raw_product_data.get('brand'),
                    'averageRating':  raw_product_data.get('averageRating'),
                    #'manufacturerName':  raw_product_data.get('manufacturerName'),
                    'shortDescription':  raw_product_data.get('shortDescription'),
                    #'thumbnailUrl':  raw_product_data['imageInfo'].get('thumbnailUrl'),
                    'price':  raw_product_data['priceInfo']['currentPrice'].get('price'),
                    #'currencyUnit':  raw_product_data['priceInfo']['currentPrice'].get('currencyUnit'),
                })

    except Exception as e:
        print('Error', e)


print(product_data_list)

import json

# Your existing code to retrieve product_data_list

# Define the file path where you want to save the JSON file
output_file_path = "product_data.json"

# Write product_data_list to a JSON file
with open(output_file_path, "w") as json_file:
    json.dump(product_data_list, json_file)

print("Data exported to", output_file_path)


with open('product_data.json', 'r') as file:
    data = json.load(file)

cleaned_data = []
for item in data:
  rating = item['averageRating']
  if item['averageRating'] is not None:
    rating = format(float(item['averageRating']), ".2f")
  elif item['averageRating'] is None:
    rating = "No Rating Found"
  cleaned_entry = {'Type': item['type'], 'Name':item['name'], 'Price': item['price'], 'Average Rating': rating}
  cleaned_data.append(cleaned_entry)

cleaned_data.sort(key=lambda x: (x['Type'],x['Price']))
table_headers = cleaned_data[0].keys()
table_data = [entry.values() for entry in cleaned_data]

print(tabulate(table_data, headers=table_headers, tablefmt='simple_grid'))

import csv

csv_file_path = 'output.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=table_headers)
    csv_writer.writeheader()
    csv_writer.writerows(cleaned_data)

print(f'Data exported to {csv_file_path}')
