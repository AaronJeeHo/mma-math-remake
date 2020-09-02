"""
Author: Aaron Ho
Python Version: 3.7
"""

import requests
import re
from bs4 import BeautifulSoup


def get_sources(link):
    """
    Get urls containing list of fighters by last name
    :param str link: URL to first page of fighters
                            http://www.espn.com/mma/fighters
    :return list: returns list of urls going to pages containing
                all fighters in alphabetical order
    """
    response = requests.get(link)
    src = response.content

    soup = BeautifulSoup(src, 'lxml')
    page_links = soup.find_all(href=re.compile(r'\?search'))
    return_list = [f"{link}{i['href']}" for i in page_links]
    return_list.insert(0, f"{link}?search=a")

    return return_list


def get_fighters(link):
    """
    Get links directly to fighter pages
    :param str link: URL going to a source page
    :return list: Return list of links going directly to fighter pages
    """
    base_url = link.split(r'/mma/fighter')[0]

    response = requests.get(link)
    src = response.content

    soup = BeautifulSoup(src, 'lxml')
    page_links = soup.find_all(href=re.compile(r'/mma/fighter/_/id/'))

    return [f"{base_url}{i['href']}" for i in page_links]


def build_url_db(source_url):
    """
    Build databases containing URLS to sources and fighters
    :param str source_url: URL to first page of fighters
                            http://www.espn.com/mma/fighters
    """
    source_list = get_sources(source_url)
    with open('../data/urls/source_urls.txt', 'w') as s_file:
        s_file.write('\n'.join(source_list))
        print("Source URLs updated")

    print('Updating fighter URLs')
    for source in source_list:
        fighter_links = get_fighters(source)
        with open(f'../data/urls/fighters_{source[-1]}.txt', 'w') as f_file:
            f_file.write('\n'.join(fighter_links))

    print('Fighter URLs updated')


def main():
    build_url_db('http://www.espn.com/mma/fighters')


if __name__ == '__main__':
    main()
