"""
Author: Aaron Ho
Python Version: 3.7
"""

import sys
import pandas as pd
from pathlib import Path
from _collections import deque


class FightGraph:
    def __init__(self):
        self.graph = {}
        self.prev = {}
        self.dist = {}
        self.path_found = False
        self.shortest = sys.maxsize

    def add_fighter(self, fighter, wins):
        self.graph[fighter] = wins


def get_wins(fight_file):
    try:
        df = pd.read_csv(f'{fight_file}/fight_records.txt', sep='\t',
                         usecols=[0, 1], names=['opponent', 'res'])

        return tuple(df.loc[df['res'] == 'W']['opponent'])

    except FileNotFoundError:
        return None


def get_losses(fight_file):
    try:
        df = pd.read_csv(f'{fight_file}/fight_records.txt', sep='\t',
                         usecols=[0, 1], names=['opponent', 'res'])

        return tuple(df.loc[df['res'] != 'W']['opponent'])

    except FileNotFoundError:
        return None


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

    if fighter_a == fighter_b:
        print(f'{fighter_a} can beat {fighter_b}')
        return None

    fight_history = FightGraph()
    to_add = deque([fighter_a])
    fight_history.dist[fighter_a] = 0
    visited = {fighter_a}

    print('Finding path...')
    while len(to_add) > 0:
        curr_fighter = to_add.popleft()
        fighter_wins = get_wins(name_to_file(curr_fighter))

        if fighter_wins is None or len(fighter_wins) < 1:
            continue
        else:
            if fighter_b in fighter_wins:
                fight_history.path_found = True
                next_dist = int(fight_history.dist[curr_fighter]) + 1

                if next_dist < fight_history.shortest:
                    fight_history.prev[fighter_b] = curr_fighter
                    fight_history.dist[fighter_b] = next_dist
                    fight_history.shortest = next_dist
                    print(f"Path found with length {next_dist}")
            else:
                fight_history.add_fighter(curr_fighter, fighter_wins)
                next_dist = int(fight_history.dist[curr_fighter]) + 1

                if next_dist < fight_history.shortest - 1:

                    for i in fighter_wins:
                        if i not in visited:
                            to_add.append(i)
                            visited.add(i)
                            fight_history.prev[i] = curr_fighter
                            fight_history.dist[i] = next_dist

                        elif fight_history.dist[i] > next_dist:
                            fight_history.dist[i] = next_dist
                            fight_history.prev[i] = curr_fighter

    if fight_history.path_found is True:
        return fight_history
    else:
        print('No path to victory found')
        return None


def get_path(f_graph, fighter_a, fighter_b):
    path = []
    curr_fighter = fighter_b
    path.append(fighter_b)

    while curr_fighter != fighter_a:
        curr_fighter = f_graph.prev[curr_fighter]
        path.append(curr_fighter)

    path.reverse()
    return path


def mma_math(fighter_a, fighter_b):
    graph = make_graph(fighter_a, fighter_b)
    path = get_path(graph, fighter_a, fighter_b)

    return path


def main():
    f1 = 'Henry Cejudo'
    f2 = 'Stipe Miocic'
    path = mma_math(f1, f2)

    print(' -> '.join(path))


if __name__ == '__main__':
    main()
