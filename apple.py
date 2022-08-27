import re
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def parse():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    URL = 'https://store77.net/apple_macbook/'

    r = requests.get(url=URL, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'lxml')

    title_mac = soup.find_all('div', class_='bp_product_img')
    price_mac = soup.find_all('p', class_='bp_text_price bp_width_fix')


    list_image_mac = [x.get('src') for i in title_mac  for x in i.find_all('img')]
    list_name_mac = [x.get('title') for i in title_mac  for x in i.find_all('img')]
    list_price = [''.join(re.findall(r'\d+', str(i))) for i in price_mac]
    list_zip = list(zip(list_name_mac,list_price,list_image_mac))
    return list_zip

parse()