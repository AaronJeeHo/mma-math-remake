"""
Author: Aaron Ho
Python Version: 3.7
"""

import pandas as pd
from pathlib import Path
from _collections import deque


class FightGraph:
    def __init__(self):
        self.graph = {}

    def add_fighter(self, fighter, wins):
        self.graph[fighter] = wins


def get_wins(fight_file):
    try:
        df = pd.read_csv(f'{fight_file}/fight_records.txt', sep='\t',
                         usecols=[0, 1], names=['opponent', 'res'])

        return tuple(df.loc[df['res'] == 'W']['opponent'])

    except FileNotFoundError:
        print('Fighter not found')
        return None


def get_losses(fight_file):
    df = pd.read_csv(f'{fight_file}/fight_records.txt', sep='\t',
                     usecols=[0, 1], names=['opponent', 'res'])

    return tuple(df.loc[df['res'] != 'W']['opponent'])


def name_to_file(name):
    n_list = name.lower().replace("-", ' ').split(' ')
    d_name = '-'.join(n_list).replace("'", '').replace(".", '')

    if len(n_list) > 2:
        for n in n_list:
            if Path(f"../data/fighters/{n[0]}-fighters/{d_name}").is_dir():
                return f"../data/fighters/{n[0]}-fighters/{d_name}"
    else:
        return f"../data/fighters/{n_list[-1][0]}-fighters/{d_name}"


def make_graph(fighter_a, fighter_b):
    """
    Creates a graph seeing if Fighter A can beat Fighter B
    :param str fighter_a: Name of fighter
    :param str fighter_b: Name of fighter
    :return: FighterGraph
    """

    if len(get_losses(name_to_file(fighter_b))) < 1:
        print('No path, fighter is undefeated')
        return None

    fight_history = FightGraph()
    to_add = deque([fighter_a])

    print('Finding path...')
    while len(to_add) > 0:
        curr_fighter = to_add.popleft()

        if curr_fighter in fight_history.graph:
            continue

        fighter_wins = get_wins(name_to_file(curr_fighter))

        if curr_fighter == fighter_b:
            fight_history.add_fighter(curr_fighter, fighter_wins)
            print(f"Graph created with {len(fight_history.graph)} nodes!")
            return fight_history

        elif fighter_wins is None or len(fighter_wins) < 1:
            continue

        else:
            if fighter_b in fighter_wins:
                to_add.appendleft(fighter_b)
            else:
                fight_history.add_fighter(curr_fighter, fighter_wins)
                to_add.extend(fighter_wins)

    print('No path to victory found')
    return None


def path_finder(graph, fighter_a, fighter_b):
    pass




def main():
    make_graph('Jose Aldo', 'Derrick Lewis')






if __name__ == '__main__':
    main()
