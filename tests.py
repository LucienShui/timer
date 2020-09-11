from __future__ import absolute_import, print_function

import logging
import time
import unittest

from timer import timer

logging.basicConfig(level=logging.DEBUG)


# explicit the timer's name and it's time unit
@timer('function:add', unit='s')
def add(a, b):
    time.sleep(.1)
    return a + b


# function name is timer's name for default
@timer
def sub(a, b):
    time.sleep(.1)
    return a - b


class TestCase(unittest.TestCase):
    def test_something(self):
        # 'timer' would be timer's name by default
        with timer('time.sleep(2)'):
            time.sleep(2)

        self.assertEqual(2, add(1, 1))
        self.assertEqual(1, sub(2, 1))


if __name__ == '__main__':
    unittest.main()
