#!/usr/bin/env python
"""reducer_local.py"""

import sys


def perform_reduce():
    current_word = None
    current_count = 0
    word = None

    with open("alice_out.txt") as file:
        for line in file:
            line = line.strip()
            word, count = line.split('\t')

            try:
                count = int(count)
            except ValueError:
                continue

            if current_word == word:
                current_count += count
            else:
                if current_word:
                    print('%s\t%s' % (current_word, current_count))
                current_count = count
                current_word = word

        if current_word == word:
            print('%s\t %s' % (current_word, current_count))


if __name__ == '__main__':
    perform_reduce()
