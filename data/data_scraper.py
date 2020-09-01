"""
Author: Aaron Ho
Python Version: 3.7
"""

import requests
import re
from bs4 import BeautifulSoup


def get_fighter_list(link):
    response = requests.get(link)
    src = response.content

    soup = BeautifulSoup(src, 'html.parser')
    page_links = soup.find_all(href=re.compile(r'\?search'))

    return [f"{link}{i['href']}" for i in page_links]


def get_fighters(link):
    base_url = link.split(r'/mma/fighter')[0]

    response = requests.get(link)
    src = response.content

    soup = BeautifulSoup(src, 'html.parser')
    page_links = soup.find_all(href=re.compile(r'/mma/fighter/_/id/'))

    # fighter_list = []
    # for i in page_links:
    #     split_name = i.text.split(', ')
    #     fighter_list.append((f"{split_name[1]} {split_name[0]}", f"{base_url}{i['href']}"))

    return [f"{base_url}{i['href']}" for i in page_links]


def get_record(link):
    split_url = link.split('_')
    history_link = f"{split_url[0]}history/_{split_url[1]}"

    response = requests.get(history_link)
    src = response.content

    soup = BeautifulSoup(src, 'html.parser')

    fighter_name = soup.find('title').text.split(' Fight')[0]
    record_list = soup.find_all('tr', {'data-idx': True})

    fighter_records = []
    for record in record_list:
        s_list = record.find_all('td', class_='Table__TD')[1:-1]
        fight_stats = (fighter_name, s_list[0].a.text,
                       s_list[1].text, s_list[2].div.text,
                       s_list[3].text, s_list[4].text)

        fighter_records.append(fight_stats)

    return fighter_records


def get_page_records(link):
    fighter_links = get_fighters(link)

    for fighter in fighter_links:
        fighter_record = get_record(fighter)
        print(*fighter_record, sep='\n')


def main():
    # fighter_pages = get_fighter_list('http://www.espn.com/mma/fighters')
    # print(*fighter_pages, sep='\n')

    # fighter_links = get_fighters('http://www.espn.com/mma/fighters?search=d')
    # dfighters = get_fighters('http://www.espn.com/mma/fighters?search=d')

    # diaz_record = get_record('https://www.espn.com/mma/fighter/_/id/2335679/nate-diaz')

    # print(*diaz_record, sep='\n')

    get_page_records('http://www.espn.com/mma/fighters?search=x')




if __name__ == '__main__':
    main()
