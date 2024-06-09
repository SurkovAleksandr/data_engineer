'''
Примеры взяты отсюда - https://lab.karpov.courses/learning/355/module/3432/lesson/30407/85478/400814/
'''
import logging
import time
from datetime import datetime

from airflow import AirflowException
import requests


def get_page_count(api_url):
    """
    Get count of page in API
    :param api_url
    :return: page count
    """
    r = requests.get(api_url)
    if r.status_code == 200:
        logging.info("SUCCESS")
        page_count = r.json().get('info').get('pages')
        logging.info(f'page_count = {page_count}')
        return page_count
    else:
        logging.warning("HTTP STATUS {}".format(r.status_code))
        raise AirflowException('Error in load page count')


def get_human_count_on_page(result_json):
    """
    Get count of human in one page of character
    :param result_json
    :return: human count
    """

    human_count_on_page = 0
    for r in result_json:
        if r['species'] == 'Human':
            human_count_on_page += 1

        logging.info(f'human_count_on_page = {human_count_on_page}')
        return human_count_on_page


def load_ram_func():
    """
    Logging count of Human in Rick&Morty
    """
    human_count = 0
    ram_char_url = 'https://rickandmortyapi.com/api/character/?page={pg}'
    page_count = get_page_count(ram_char_url.format(pg='1'))
    for page in range(page_count):
        r = requests.get(ram_char_url.format(pg=str(page + 1)))
        if r.status_code == 200:
            logging.info(f'PAGE {page + 1}')
            human_count += get_human_count_on_page(r.json().get('results'))
        else:
            logging.warning("HTTP STATUS {}".format(r.status_code))
            raise AirflowException('Error in load from Rick&Morty API')
    logging.info(f'Humans in Rick&Morty: {human_count}')


#load_ram_func()

page = 0
ram_url = 'https://rickandmortyapi.com/api/location?page={page_number}'
locations = []

response = requests.get(ram_url.format(page_number=str(page + 1)))
if response.status_code == 200:
    logging.info(f'PAGE {page + 1}')
    results = response.json().get('results')
    for r in results:
        locations.append(r)#[r['name']] = len(r['residents'])
else:
    logging.warning("HTTP STATUS {}".format(response.status_code))
    raise AirflowException('Error in load from Rick&Morty API')

#print(locations)

#print(sorted(locations, key=locations, reverse=True))
l = sorted(locations, key=lambda x: len(x['residents']), reverse=True)[:3]
for loc in l:
    print(f"INSERT INTO public.al_surkov_ram_location VALUES ({loc['id']}, '{loc['name']}', '{loc['type']}', '{loc['dimension']}', {len(loc['residents'])}), {datetime.now()}")