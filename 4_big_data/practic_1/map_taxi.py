#!/usr/bin/env python3
import datetime
import re
import sys

mapping = {
    1: 'Credit card',
    2: 'Cash',
    3: 'No charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided trip'
}

date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def map_taxi():
    # with open("yellow_tripdata_2020-05.csv") as file:
    #    for line in file:
    for line in sys.stdin:
        line = line.strip()
        words = line.split(',')

        row = validate_and_extract(words)
        if not row:
            continue

        print('%s,%s\t%s' % (row['period'], row['payment'], row['amount']))


def validate_and_extract(columns):
    try:
        # Проверка поля tpep_pickup_datetime
        tpep_pickup_datetime = datetime.datetime.fromisoformat(columns[1])
    except ValueError as ex:
        #print(f'Error: {ex}. Row: {columns}')
        return None

    if tpep_pickup_datetime.year != 2020:
        return None

    try:
        key = int(columns[9])
    except ValueError as ex:
        #print(f'Error: {ex} in row: {columns}')
        return None

    if key not in mapping.keys():
        # Проверка поля payment_type
        #print(f'Error: not found payment_type({columns[9]}) in row: {columns}')
        return None

    payment_type = mapping[key]

    try:
        # Проверка поля tip_amount
        tip_amount = float(columns[13])
    except ValueError as ex:
        #print(f'Error: {ex} in row: {columns}')
        return None

    month = '{:02d}'.format(tpep_pickup_datetime.month)

    return {
        'period': f'{tpep_pickup_datetime.year}-{month}',
        'payment': payment_type,
        'amount': tip_amount
    }


if __name__ == '__main__':
    map_taxi()
