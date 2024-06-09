#!/usr/bin/env python3

import sys


def reducer_taxi():
    sum_amount = 0.0
    year_and_type = None
    current_year_and_type = None

    for line in sys.stdin:
        line = line.strip()

        try:
            year_and_type, amount = line.split('\t', 1)
            amount = float(amount)
        except ValueError:
            continue

        if current_year_and_type == year_and_type:
            sum_amount += amount
        else:
            if current_year_and_type:
                print('%s,%s' % (current_year_and_type, sum_amount))
            sum_amount = amount
            current_year_and_type = year_and_type

    if current_year_and_type == year_and_type:
        print('%s,%s' % (current_year_and_type, sum_amount))


if __name__ == '__main__':
    reducer_taxi()
