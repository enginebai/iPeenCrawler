import requests
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"
ROOT_URL = 'http://www.ipeen.com.tw'
LIST_URL = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'

def get_shop_link_list():
    list_req = requests.get(LIST_URL)
    if list_req.status_code == requests.codes.ok:
        soup = BeautifulSoup(list_req.content, HTML_PARSER)
        shop_links_a_tags = soup.find_all('a', attrs={'data-label': '店名'})

        shop_links = []
        for link in shop_links_a_tags:
            print(ROOT_URL + link['href'])
            shop_links.append(ROOT_URL + link['href'])


if __name__ == '__main__':
    get_shop_link_list()