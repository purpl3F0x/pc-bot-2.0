import os
import random

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)

f = open(current_file_dir + "/quotes.txt", 'r', encoding='utf-8')

quotes = f.read().split('\n\n\n')


def quote():
    '''Returns a random quote'''
    return (random.choice(quotes))


if __name__ == '__main__':
    print(quote())
