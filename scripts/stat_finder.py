"""
Author: Aaron Ho
Python Version: 3.7
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


def name_to_url(name):
    n_list = name.lower().replace("-", ' ').split(' ')
    d_name = '-'.join(n_list).replace("'", '').replace(".", '')

    if len(n_list) > 2:
        for n in n_list:
            with open(f"../data/urls/fighters_{n[0]}.txt", 'r') as file:
                for line in file:
                    if d_name in line:
                        return line.rstrip()
    else:
        with open(f"../data/urls/fighters_{n_list[-1][0]}.txt", 'r') as file:
            for line in file:
                if d_name in line:
                    return line.rstrip()

    return None


def scrape_stats(link):
    split_url = link.split('_')
    stat_link = f"{split_url[0]}stats/_{split_url[1]}"

    response = requests.get(stat_link)
    src = response.content

    soup = BeautifulSoup(src, 'lxml')

    print(soup.prettify())


def main():
    # fighter_url = name_to_url('Khabib Nurmagomedov')
    # scrape_stats(fighter_url)


if __name__ == '__main__':
    main()
