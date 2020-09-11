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


def name_links():
    """
    Get fighter names alongside their links
    """
    with open('../data/urls/source_urls.txt', 'r') as s_file:
        source_list = [line.rstrip() for line in s_file]

    base_url = (source_list[0]).split(r'/mma/fighter')[0]

    with open('../data/urls/name_url.tsv', 'w') as name_file:
        for source_page in source_list:
            response = requests.get(source_page)
            src = response.content

            soup = BeautifulSoup(src, 'lxml')
            page_links = soup.find_all(href=re.compile(r'/mma/fighter/_/id/'))

            for f_link in page_links:
                split_name = f_link.text.split(', ')
                f_name = f"{split_name[1]} {split_name[0]}"
                name_file.write(f"{f_name}\t{base_url}{f_link['href']}\n")

            print(f"Name URL pairs in {source_page} written!")


def main():
    # build_url_db('http://www.espn.com/mma/fighters')
    # name_links()
    pass



if __name__ == '__main__':
    main()
