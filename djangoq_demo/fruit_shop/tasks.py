import time


def order_fruit(fruit, num_fruit):
    time.sleep(num_fruit)
    return (
        '{fruit}_{num_fruit:d}'
        .format(fruit=fruit, num_fruit=num_fruit)
    )
