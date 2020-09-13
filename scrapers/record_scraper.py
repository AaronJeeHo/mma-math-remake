"""
Author: Aaron Ho
Python Version: 3.7
"""

import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from scripts.stat_finder import name_to_url


def update_record(link):
    split_url = link.split('_')
    history_link = f"{split_url[0]}history/_{split_url[1]}"

    try:
        df_record = (pd.read_html(history_link)[0])[['Opponent', 'Res.']]
        file_pre = link.split('/')[-1]
        file_name = f"../data/fighters/{file_pre}.tsv"
        df_record.to_csv(file_name, sep='\t', index=False, header=False)
        print(f"{file_pre}.tsv written!")

    except ImportError:
        print('Database not written')
        return None


def build_all_records(name_urls):
    """
    Retrieves records for ALL fighters
    WILL TAKE A LONG TIME!!!
    :param str name_urls: File containing fighter urls
    """
    name_db = pd.read_csv(name_urls, sep='\t',
                          header=None, names=['name', 'link'])
    url_list = list(name_db['link'])

    for link in url_list:
        update_record(link)

    print('ALL RECORDS FOUND!')



# def get_record(link):
#     split_url = link.split('_')
#     history_link = f"{split_url[0]}history/_{split_url[1]}"
#
#     response = requests.get(history_link, timeout=10)
#     src = response.content
#
#     soup = BeautifulSoup(src, 'lxml')
#
#     record_list = soup.find_all('tr', {'data-idx': True})
#
#     if 0 >= len(record_list):
#         return
#
#     else:
#
#         fighter_records = []
#         for record in record_list:
#             s_list = record.find_all('td', class_='Table__TD')[1:-2]
#
#             if (s_list[0].a is not None) and (s_list[1].div is not None):
#                 fight_stats = (s_list[0].a.text, s_list[1].div.text,
#                                s_list[2].text, s_list[3].text)
#
#                 fighter_records.append(fight_stats)
#
#         return fighter_records


# def build_record_db(fighter_urls):
#     """
#     Build record database for fighters with urls denoted
#     :param str fighter_urls: file containing fighter URLs
#     """
#     name_char = fighter_urls.split('.txt')[0][-1]
#     print(f'Creating {name_char}-fighters database...')
#
#     with open(fighter_urls, 'r') as url_file:
#         url_list = [line.rstrip() for line in url_file]
#
#     print(f'{len(url_list)} fighters found')
#
#     for fighter_link in url_list:
#         name = fighter_link.split('/')[-1]
#         fight_record = get_record(fighter_link)
#         print(name)
#
#         if fight_record is not None:
#             dir_loc = f'../data/fighters/{name_char}-fighters/{name}'
#
#             Path(dir_loc).mkdir(parents=True, exist_ok=True)
#
#             with open(f'{dir_loc}/fight_records.txt', 'w', newline='') as file:
#                 tsv_writer = csv.writer(file, delimiter='\t')
#                 tsv_writer.writerows(fight_record)
#
#     print(f'{name_char}-fighters database created!')


# def build_all_records(url_dir):
#     """
#     Retrieves records for ALL fighters
#     WILL TAKE A LONG TIME!!!
#     :param str url_dir: url_dir location
#     """
#
#     url_files = Path(url_dir).glob('fighters*')
#
#     for link_files in url_files:
#         build_record_db(str(link_files))
#
#     print('ALL RECORDS FOUND!')


def main():
    # update_record('https://www.espn.com/mma/fighter/_/id/2504951/stipe-miocic')
    build_all_records('../data/urls/name_url.tsv')



if __name__ == '__main__':
    main()
