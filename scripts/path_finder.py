"""
Author: Aaron Ho
Python Version: 3.7
"""

import pandas as pd
from _collections import deque


def get_wins(fight_file):
    df = pd.read_csv(f'{fight_file}/fight_records.txt', sep='\t',
                     usecols=[0, 1], names=['opponent', 'res'])

    return list(df.loc[df['res'] == 'W']['opponent'])


def name_to_file(name):
    n_list = name.lower().split(' ')
    return f"../data/fighters/{n_list[-1][0]}-fighters/{'-'.join(n_list)}"


def main():
    wins = get_wins('../data/fighters/n-fighters/khabib-nurmagomedov')
    # test = wins[0]

    print(name_to_file('Abdul-Kerim Edilov'))


if __name__ == '__main__':
    main()
