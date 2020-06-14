import json

import cars as cars
import requests
from bs4 import BeautifulSoup

# Здесь должна быть ссылка на контретный тип авто

# попробуйте указать свои данные, но скорее всего все итак будет работать
#библеотеки скачать не забудьте
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/83.0.4103.97 Safari/537.36','accept':'*/*' }
HOST = 'kolesa.kz'



def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html,'html.parser')
    pagination = soup.find('div', class_='pager').find_all(['li'])

    if pagination:

        return int(pagination[-1].get_text())
    else:
        return 1





def total_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination1 = soup.find('div', class_='pager').find_all(['li'])
    page1_count = len(pagination1)

    print(page1_count)


def get_context(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div', ['row vw-item list-item a-elem',
                                  'row vw-item list-item blue a-elem',
                                  'row vw-item list-item yellow a-elem'])


    cars = []
    for item in items:

        in_credit =item.find('div', class_='month-price')
        if in_credit:
            in_credit = in_credit.get_text(strip=True)
        else:
            in_credit = " Возможности в кредит нет !"
        in_credit = in_credit.replace(u'\xa0', u' ')

        cars.append({
                'title': item.find('span', class_='a-el-info-title').get_text(strip=True),
                #'description': item.find('div',class_='desc').get_text(strip=True),
                'credit': in_credit,
                'price':item.find('span', class_='price').get_text(strip=True).replace(u'\xa0', u' '),

                'link': HOST+ item.find('a', class_='list-link ddl_product_link').get('href'),
            })
    return cars

    #тут я все сохраняю в json




def parse():
    URL= input('Enter url:')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:


        cars = []
        pages_count = get_pages_count(html.text)
        print(pages_count)
        for page in range(1,11):
            # Здесб я указал всего 4 строниц потому что там по 100-300 страниц авто это очень долго если хотите можете поменять значения
            print(f'Parsing web {page}, from {10}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_context(html.text))
        print(cars)
        with open('cars.json', 'w', encoding='utf-8') as file:
            json.dump(cars, file, indent=2, ensure_ascii=False)

    else:
        print('Cannot connect to the website!')

parse()
