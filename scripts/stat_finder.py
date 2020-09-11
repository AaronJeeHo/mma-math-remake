"""
Author: Aaron Ho
Python Version: 3.7
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def name_to_url(db, name):
    link = list(db.loc[db['name'] == name]['link'])

    if len(link) > 0:
        return link[0]
    else:
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


def scrape_ratio(link):
    # link = name_to_url(f_name)
    split_url = link.split('_')
    stat_link = f"{split_url[0]}stats/_{split_url[1]}"

    try:
        response = requests.get(stat_link, timeout=10)
        src = response.content

        soup = BeautifulSoup(src, 'lxml')
        record_list = soup.find_all('div', class_='StatBlockInner__Value')

        if len(record_list) == 3:
            win_loss = tuple(map(int, record_list[0].text.split('-')))
            ko = tuple(map(int, record_list[1].text.split('-')))
            sub = tuple(map(int, record_list[2].text.split('-')))

            return {'WLD': win_loss, 'KO': ko, 'SUB': sub}
        else:
            return None

    except ImportError:
        return None


def scrape_stats(link):
    # link = name_to_url(f_name)
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
                              (striking['SSA'].astype(str) != '0')][['SSL', 'SSA']]

        # sig_attempted = sum(t_sigs['SSA'].astype(float))

        if t_sigs.empty:
            sig_r = 0
        else:
            sig_r = round((sum(t_sigs['SSL'].astype(float)) /
                           sum(t_sigs['SSA'].astype(float))), 2) * 100

        total_s = striking.loc[striking['TSL-TSA'] != '-'][['TSL-TSA']]

        targets = striking.loc[((striking['%BODY'] != '0%') |
                                (striking['%HEAD'] != '0%') |
                                (striking['%LEG'] != '0%')) &
                               (striking['%BODY'] != '-') &
                               (striking['%HEAD'] != '-') &
                               (striking['%LEG'] != '-')][['%BODY',
                                                           '%HEAD', '%LEG']]

        # Get clinch stats
        clinch = df_list[1]

        takedowns = clinch.loc[((clinch['TDL'].astype(str) != '0') |
                                (clinch['TDA'].astype(str) != '0')) &
                               (clinch['TDL'] != '-') &
                               (clinch['TDA'] != '-')]

        # td_attempted = sum(takedowns['TDA'].astype(float))

        if takedowns.empty:
            td_a = 0
        else:
            td_a = round((sum(takedowns['TDL'].astype(float)) /
                          sum(takedowns['TDA'].astype(float))), 2) * 100

        # Get ground stats
        ground = df_list[2]

        body_gs = ground.loc[(ground['SGBA'].astype(str) != '0') &
                             (ground['SGBA'] != '-') &
                             (ground['SGBL'] != '-')][['SGBL', 'SGBA']]

        #bgs_attempted = sum(body_gs['SGBA'].astype(float))

        if body_gs.empty:
            bgs_a = 0
        else:
            bgs_a = round((sum(body_gs['SGBL'].astype(float)) /
                           sum(body_gs['SGBA'].astype(float))), 2) * 100

        head_gs = ground.loc[(ground['SGHA'].astype(str) != '0') &
                             (ground['SGHA'] != '-') &
                             (ground['SGHL'] != '-')][['SGHL', 'SGHA']]

        # hgs_attempted = sum(head_gs['SGHA'].astype(float))

        if head_gs.empty:
            hgs_a = 0
        else:
            hgs_a = round((sum(head_gs['SGHL'].astype(float)) /
                           sum(head_gs['SGHA'].astype(float))), 2) * 100

        leg_gs = ground.loc[(ground['SGLA'].astype(str) != '0') &
                            (ground['SGLA'] != '-') &
                            (ground['SGLL'] != '-')][['SGLL', 'SGLA']]

        # lgs_attempted = sum(leg_gs['SGLA'].astype(float))
        # print(lgs_attempted)
        # print(leg_gs)
        if leg_gs.empty:
            lgs_a = 0
        else:
            lgs_a = round((sum(leg_gs['SGLL'].astype(float)) /
                           sum(leg_gs['SGLA'].astype(float))), 2) * 100

        sub_a = sum((ground.loc[(ground['SM'].astype(str) != '0') &
                                (ground['SM'] != '-')]['SM']).astype(int))

        stats_only = ground.loc[:, 'SGBL':'SM']
        active_stats = ((stats_only != '0') & (stats_only != '-')).any(axis=1)

        num_stats = sum(list(active_stats))

        # Process stats into dict
        striking_stats = {'Head Strike Accuracy': frac_to_stats(head_s),
                          'Body Strike Accuracy': frac_to_stats(body_s),
                          'Leg Strike Accuracy': frac_to_stats(leg_s),
                          'Significant Strike Accuracy': sig_r,
                          'Total Strike Accuracy':
                              percent_to_stats(total_s, 'TSL-TSA'),
                          'Breakdown Head': percent_to_stats(targets, '%HEAD'),
                          'Breakdown Body': percent_to_stats(targets, '%BODY'),
                          'Breakdown Leg': percent_to_stats(targets, '%LEG')
                          }

        clinch_stats = {'Takedown Accuracy': td_a}

        ground_stats = {'Ground Head Strike Accuracy': hgs_a,
                        'Ground Body Strike Accuracy': bgs_a,
                        'Ground Leg Strike Accuracy': lgs_a,
                        'Sub Attempts Per Fight': round((sub_a/num_stats), 2)
                        }
        # print(f'{f_name} Stats Found!')
        return striking_stats, clinch_stats, ground_stats

    except ImportError:
        print('Stats not found')
        return None


def get_header_img(link):
    response = requests.get(link, timeout=10)
    src = response.content
    # src = urlopen(link)
    soup = BeautifulSoup(src, 'html.parser')
    img_link = None
    f_name = None
    l_name = None

    headshot = soup.find_all('figure', class_='PlayerHeader__HeadShot')
    name_header = soup.find_all('h1', class_='PlayerHeader__Name')

    if len(headshot) > 0:
        # img_list = (headshot[0].find_all('img'))
        split_id = link.split('id/')[-1]
        id_num = split_id.split('/')[0]
        img_link = (f"https://a.espncdn.com/combiner/i?img=/i/headshots/"
                    f"mma/players/full/{id_num}.png&w=350&h=254")

    if len(name_header) > 0:
        name_list = name_header[0].find_all('span')
        f_name = name_list[0].text
        l_name = name_list[1].text

    return img_link, f_name, l_name


def main():
    name_db = pd.read_csv('../data/urls/name_url.tsv',
                          sep='\t', header=None, names=['name', 'link'])
    #link = name_to_url(name_db, 'Khabib Nurmagomedov')
    # link = name_to_url(name_db, 'Daniel Cormier')
    # stats = scrape_stats(link)
    # print(stats)
    pass


if __name__ == '__main__':
    main()
