import requests
import random 
from bs4 import BeautifulSoup

def anecdot():
    URL_ = 'https://nekdo.ru/random/'
    r = requests.get(url=URL_)
    soup = BeautifulSoup(r.text,'lxml')
    text = soup.find_all('div',class_='text')
    random_num = random.randint(0,15)
    return text[random_num].text