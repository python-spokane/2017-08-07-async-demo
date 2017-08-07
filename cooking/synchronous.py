#
# synchronous.py
#
# author: Franco Gasperino

"""
Preparing meals in the kitchen using a simple, synchronous execution model.

Dad has 3 kids, and gives them each the choice of mac & cheese, chicken noodle soup,
or chicken nuggets. Each meal has several steps to complete.

Each step of the meal will contain a sleep. This simulates a time taken to complete the
step. Some of these sleeps are indicative of actual work taking time, while others are
time taken waiting on something to complete.

Dad is going to handle each meal sequentially, start to finish.
"""

from time import time, sleep


def prepare(kid, meal):

    seconds = 2
    print('{} - Preparing {} by with container for {} seconds.'.format(kid, meal, seconds))
    sleep(seconds)


def cook(kid, meal):

    seconds = 5
    print('{} - Cooking {}. Will stare blankly at the stove top for {} seconds now.'.format(kid, meal, seconds))
    sleep(seconds)


def boil(kid, meal):

    seconds = 3
    print('{} - Boiling water for {} for {} seconds.'.format(kid, meal, seconds))
    sleep(seconds)


def microwave(kid, meal):

    seconds = 2
    print('{} - Turning {} into soggy mush in the microwave. ETA {} seconds.'.format(kid, meal, seconds))
    sleep(seconds)


def cool(kid, meal):

    seconds = 1
    print('{} - The {} is cooling for {}.'.format(kid, meal, seconds))
    sleep(seconds)


def serve(kid, meal):

    seconds = 1
    print('{} - Dinner is served. Your favorite: {}.'.format(kid, meal))
    sleep(seconds)


if __name__ == '__main__':

    # Meals that dad is willing to cook and the steps.
    meals = {
        'mac & cheese': (prepare, boil, cook, cool, serve),
        'chicken noodle soup': (prepare, cook, cool, serve),
        'chicken nuggets': (prepare, microwave, cool, serve)
    }

    # The 3 kids and their meals.
    orders = (
        {'kid': 'joe',  'meal': 'mac & cheese'},
        {'kid': 'jake', 'meal': 'chicken noodle soup'},
        {'kid': 'jane', 'meal': 'chicken nuggets'}
    )

    start = int(time())

    for order in orders:
        for step in meals[order['meal']]:
            step(order['kid'], order['meal'])

    end = int(time())

    print('')
    print('Dinner done in {} seconds.'.format(end - start))
