import requests
from bs4 import BeautifulSoup
import re

HTML_PARSER = "html.parser"
ROOT_URL = 'http://www.ipeen.com.tw'
LIST_URL = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
SHOP_PATH = 'shop/'
SPACE_RE = re.compile(r'\s+')


def get_shop_link_list():
    list_req = requests.get(LIST_URL)
    if list_req.status_code == requests.codes.ok:
        soup = BeautifulSoup(list_req.content, HTML_PARSER)
        shop_links_a_tags = soup.find_all('a', attrs={'data-label': '店名'})

        shop_links = []
        for link in shop_links_a_tags:
            shop_link = ROOT_URL + link['href']
            print(shop_link)
            shop_links.append(shop_link)
            parse_shop_information(shop_link)


def parse_shop_information(shop_link):
    shop_id = re.sub(re.compile(r'^.*/' + SHOP_PATH), '', shop_link).split('-')[0]
    print(shop_id)

    req = requests.get(shop_link)
    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, HTML_PARSER)
        shop_header_tag = soup.find('div', id='shop-header')
        name_tag = shop_header_tag.find('span', attrs={'itemprop': 'name'})
        print(re.sub(SPACE_RE, '', name_tag.text))
        category_tag = shop_header_tag.find("p", class_={'cate i'})
        print(re.sub(SPACE_RE, '', category_tag.a.text))
        address_tag = shop_header_tag.find('a', attrs={'data-label': '上方地址'})
        print(re.sub(SPACE_RE, '', address_tag.text))

        gps_str = address_tag['href']
        # print(gps_str)
        gps_str = re.search('/c=(\d+.\d*),(\d+.\d*)/', gps_str).group().replace('/', '')
        # print(gps_str)
        lat = gps_str.split(',')[0]
        lng = gps_str.split(',')[1]
        print(lat.split('=')[1], lng)


if __name__ == '__main__':
    get_shop_link_list()