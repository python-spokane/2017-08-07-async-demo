#
# asynchronous.py
#
# author: Franco Gasperino

"""
Preparing meals in the kitchen using a concurrent execution model.

Dad has 3 kids, and gives them each the choice of mac & cheese, chicken noodle soup,
or chicken nuggets. Each meal has several steps to complete.

Dad is going to concurrently cook the meals. Each step which would cause dad to wait on
completion (aka "block") that do not require his attention, he will switch to handling
another task waiting on him.
"""

from time import time, sleep
import asyncio


async def prepare(kid, meal):

    seconds = 2
    print('{} - Preparing {} by with container for {} seconds.'.format(kid, meal, seconds))
    sleep(seconds)


async def cook(kid, meal):

    seconds = 5
    print('{} - Cooking {} for {} seconds. Switching to another meal.'.format(kid, meal, seconds))
    await asyncio.sleep(seconds)


async def boil(kid, meal):

    seconds = 3
    print('{} - Boiling water for {} for {} seconds. Switching to another meal.'.format(kid, meal, seconds))
    await asyncio.sleep(seconds)


async def microwave(kid, meal):

    seconds = 2
    print('{} - Microwaving {} for {} seconds. Switching to another meal.'.format(kid, meal, seconds))
    await asyncio.sleep(seconds)


async def cool(kid, meal):

    seconds = 1
    print('{} - The {} is cooling for {}. Switching to another meal.'.format(kid, meal, seconds))
    await asyncio.sleep(seconds)


async def serve(kid, meal):

    print('{} - Dinner is served. Your favorite: {}.'.format(kid, meal))


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

    # The dinner task, start to finish.
    async def make_dinner(order):
        for step in meals[order['meal']]:
            await step(order['kid'], order['meal'])

    start = int(time())

    # Create 3 dinner tasks, one for each kid.
    tasks = [asyncio.Task(make_dinner(order)) for order in orders]

    # Make the dinners concurrently.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))

    end = int(time())

    print('')
    print('Dinner done in {} seconds.'.format(end - start))
