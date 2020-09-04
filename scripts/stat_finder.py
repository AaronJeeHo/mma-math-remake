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


def frac_to_stats(stats):
    """
    Parse stats represented as fraction
    :param list stats:
    :return:
    """
    landed = 0
    attempt = 0

    for frac in stats:
        split_vals = frac.split('/')
        landed += int(split_vals[0])
        attempt += int(split_vals[1])

    return round((landed / attempt) * 100, 2)


def percent_to_stats(df, col):
    """
    Return dataframe col of percentages as stats
    :param DataFrame df:
    :param str col:
    :return:
    """

    return round(df[col].str.rstrip('%').astype('float').mean(), 2)



def scrape_stats(link):
    split_url = link.split('_')
    stat_link = f"{split_url[0]}stats/_{split_url[1]}"

    try:
        df_list = pd.read_html(stat_link)

        # Get striking stats
        striking = df_list[0]

        body_s = list(striking.loc[(striking['SDBL/A'] != '-') &
                                   (striking['SDBL/A'] != '0/0')]['SDBL/A'])

        head_s = list(striking.loc[(striking['SDHL/A'] != '-') &
                                   (striking['SDHL/A'] != '0/0')]['SDHL/A'])

        leg_s = list(striking.loc[(striking['SDLL/A'] != '-') &
                                  (striking['SDLL/A'] != '0/0')]['SDLL/A'])

        t_sigs = striking.loc[(striking['SSL'] != '-') &
                              (striking['SSA'] != '-') &
                              (striking['SSA'] != '0')][['SSL', 'SSA']]

        targets = striking.loc[((striking['%BODY'] != '0%') |
                                (striking['%HEAD'] != '0%') |
                                (striking['%LEG'] != '0%')) &
                               (striking['%BODY'] != '-') &
                               (striking['%HEAD'] != '-') &
                               (striking['%LEG'] != '-')][['%BODY',
                                                           '%HEAD', '%LEG']]

        # Get clinch stats
        clinch = df_list[1]

        takedowns = clinch.loc[((clinch['TDL'] != '0') |
                                (clinch['TDA'] != '0')) &
                               (clinch['TDL'] != '-') &
                               (clinch['TDA'] != '-')]

        # Get ground stats
        ground = df_list[2]
        print(ground.columns)

        body_gs = ground.loc[(ground['SGBA'] != '0') &
                             (ground['SGBA'] != '-') &
                             (ground['SGBL'] != '-')][['SGBL', 'SGBA']]

        head_gs = ground.loc[(ground['SGHA'] != '0') &
                             (ground['SGHA'] != '-') &
                             (ground['SGHL'] != '-')][['SGHL', 'SGHA']]

        leg_gs = ground.loc[(ground['SGLA'] != '0') &
                             (ground['SGLA'] != '-') &
                             (ground['SGLL'] != '-')][['SGLL', 'SGLA']]

        subs = ground.loc[(ground['SM'] != '0') & (ground['SM'] != '-')]['SM']

        stats_only = ground.loc[:, 'SGBL':'SM']
        active_stats = ((stats_only != '0') & (stats_only != '-')).any(axis=1)
        num_stats = sum(list(active_stats))

        # Process stats into dict













    except ImportError:
        print('Stats not found')
        return None


def main():
    link = name_to_url('Khabib Nurmagomedov')
    scrape_stats(link)




if __name__ == '__main__':
    main()
