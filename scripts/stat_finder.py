"""
Author: Aaron Ho
Python Version: 3.7
"""

import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup

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
    try:
        landed = 0
        attempt = 0

        for frac in stats:
            split_vals = frac.split('/')
            landed += int(split_vals[0])
            attempt += int(split_vals[1])
        return round((landed / attempt) * 100, 2)

    except ZeroDivisionError:
        return 0.0


def percent_to_stats(df, col):
    """
    Return dataframe col of percentages as stats
    :param DataFrame df:
    :param str col:
    :return:
    """
    try:
        return round(df[col].str.rstrip('%').astype('float').mean(), 2)
    except ZeroDivisionError:
        return 0.0


def scrape_ratio(link):
    try:
        split_url = link.split('_')
        stat_link = f"{split_url[0]}stats/_{split_url[1]}"

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
            return {'WLD': (0, 0, 0), 'KO': (0, 0), 'SUB': (0, 0)}

    except (ImportError, TypeError, AttributeError):
        return {'WLD': (0, 0, 0), 'KO': (0, 0), 'SUB': (0, 0)}


def scrape_stats(link):
    try:
        split_url = link.split('_')
        stat_link = f"{split_url[0]}stats/_{split_url[1]}"

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

        if t_sigs.empty:
            sig_r = 0.0
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

        clinch = df_list[1]

        takedowns = clinch.loc[((clinch['TDL'].astype(str) != '0') |
                                (clinch['TDA'].astype(str) != '0')) &
                               (clinch['TDL'] != '-') &
                               (clinch['TDA'] != '-')]

        if takedowns.empty:
            td_a = 0.0
        else:
            td_a = round((sum(takedowns['TDL'].astype(float)) /
                          sum(takedowns['TDA'].astype(float))), 2) * 100

        # Get ground stats
        ground = df_list[2]

        body_gs = ground.loc[(ground['SGBA'].astype(str) != '0') &
                             (ground['SGBA'] != '-') &
                             (ground['SGBL'] != '-')][['SGBL', 'SGBA']]

        if body_gs.empty:
            bgs_a = 0.0
        else:
            bgs_a = round((sum(body_gs['SGBL'].astype(float)) /
                           sum(body_gs['SGBA'].astype(float))), 2) * 100

        head_gs = ground.loc[(ground['SGHA'].astype(str) != '0') &
                             (ground['SGHA'] != '-') &
                             (ground['SGHL'] != '-')][['SGHL', 'SGHA']]

        if head_gs.empty:
            hgs_a = 0.0
        else:
            hgs_a = round((sum(head_gs['SGHL'].astype(float)) /
                           sum(head_gs['SGHA'].astype(float))), 2) * 100

        leg_gs = ground.loc[(ground['SGLA'].astype(str) != '0') &
                            (ground['SGLA'] != '-') &
                            (ground['SGLL'] != '-')][['SGLL', 'SGLA']]

        if leg_gs.empty:
            lgs_a = 0.0
        else:
            lgs_a = round((sum(leg_gs['SGLL'].astype(float)) /
                           sum(leg_gs['SGLA'].astype(float))), 2) * 100

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
                        }

        return striking_stats, clinch_stats, ground_stats

    except (ImportError, TypeError, AttributeError):
        striking_stats = {'Head Strike Accuracy': 0.0,
                          'Body Strike Accuracy': 0.0,
                          'Leg Strike Accuracy': 0.0,
                          'Significant Strike Accuracy': 0.0,
                          'Total Strike Accuracy': 0.0,
                          'Breakdown Head': 0.0,
                          'Breakdown Body': 0.0,
                          'Breakdown Leg': 0.0
                          }

        clinch_stats = {'Takedown Accuracy': 0.0}

        ground_stats = {'Ground Head Strike Accuracy': 0.0,
                        'Ground Body Strike Accuracy': 0.0,
                        'Ground Leg Strike Accuracy': 0.0,
                        }
        return striking_stats, clinch_stats, ground_stats


def get_header_img(link):
    img_link = None
    f_name = None
    l_name = None

    if link is None:
        return img_link, f_name, l_name

    else:
        response = requests.get(link, timeout=10)
        src = response.content
        soup = BeautifulSoup(src, 'html.parser')

        headshot = soup.find_all('figure', class_='PlayerHeader__HeadShot')
        name_header = soup.find_all('h1', class_='PlayerHeader__Name')

        if len(headshot) > 0:
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
    pass


if __name__ == '__main__':
    main()
