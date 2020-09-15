"""
Author: Aaron Ho
Python Version: 3.7
"""


import shutil
import pandas as pd
from pathlib import Path
from urllib.error import HTTPError


def update_record(link):
    split_url = link.split('_')
    history_link = f"{split_url[0]}history/_{split_url[1]}"
    path = Path(__file__).parent

    try:
        df_record = (pd.read_html(history_link)[0])[['Opponent', 'Res.']]
        file_pre = link.split('/')[-1]
        file_name = path / f"../data/fighters/{file_pre}.tsv"
        df_record.to_csv(file_name, sep='\t', index=False, header=False)
        print(f"{file_pre}.tsv written!")

    except ImportError:
        print('Database not written')
        return None

    except HTTPError as err:
        print(err.code)
        print(f"Problem reaching {link}")
        print("Written to url_errors.txt")
        with open(path / "../data/urls/url_errors.txt", "a") as file:
            file.write(f"{link}\n")


def build_from_file(url_file):
    with open(url_file, 'r') as file:
        url_list = [line.rstrip() for line in file]

    for link in url_list:
        update_record(link)

    print('ALL RECORDS FOUND!')


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


def update_directories():
    path = Path(__file__).parent / "../data/fighters"
    records = Path(path).glob('*.tsv')

    for file_path in records:
        fighter_file = str(file_path).split('/')[-1]
        f_initial = fighter_file[0]

        dir_loc = path / f"{f_initial}-fighters/"
        new_path = dir_loc / fighter_file

        Path(dir_loc).mkdir(parents=True, exist_ok=True)
        shutil.move(file_path, new_path)
        print(f"Created {new_path}")


def main():
    # update_directories()
    pass


if __name__ == '__main__':
    main()
