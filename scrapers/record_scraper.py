"""
Author: Aaron Ho
Python Version: 3.7
"""

import requests
import os
import re
import csv
from bs4 import BeautifulSoup


def get_record(link):
    split_url = link.split('_')
    history_link = f"{split_url[0]}history/_{split_url[1]}"

    response = requests.get(history_link)
    src = response.content

    soup = BeautifulSoup(src, 'lxml')

    record_list = soup.find_all('tr', {'data-idx': True})

    if 0 >= len(record_list):
        return

    else:

        fighter_records = []
        for record in record_list:
            s_list = record.find_all('td', class_='Table__TD')[1:-2]

            if (s_list[0].a is not None) and (s_list[1].div is not None):
                fight_stats = (s_list[0].a.text, s_list[1].div.text,
                               s_list[2].text, s_list[3].text)

                fighter_records.append(fight_stats)

        return fighter_records


def build_record_db(fighter_urls):
    """
    Build record database for fighters with urls denoted
    :param str fighter_urls: file containing fighter URLs
    """
    name_char = fighter_urls.split('.txt')[0][-1]
    print(f'Creating {name_char}-fighters database...')

    with open(fighter_urls, 'r') as url_file:
        url_list = [line.rstrip() for line in url_file]

    for fighter_link in url_list:
        name = fighter_link.split('/')[-1]
        fight_record = get_record(fighter_link)

        if fight_record is not None:
            file_loc = (f'../data/fighters/'
                        f'{name_char}-fighters/{name}/fight_records.txt')

            with open(file_loc, 'w', newline='') as record_file:
                tsv_writer = csv.writer(record_file, delimiter='\t')
                tsv_writer.writerows(fight_record)

    print(f'{name_char}-fighters database created!')


def main():
    x_links = '../data/urls/fighters_x.txt'
    build_record_db(x_links)




if __name__ == '__main__':
    main()
