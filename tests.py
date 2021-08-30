from __future__ import absolute_import, print_function

import logging
import time
import unittest

from timer import timer, get_timer

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


class Test:
    @timer
    def say_something(self, something):
        print(something)


class TestCase(unittest.TestCase):
    def test_something(self):
        # 'timer' would be timer's name by default
        with timer('time.sleep(2)') as t:
            time.sleep(1)
            print(f'after time.sleep(1) once, t.elapse = {t.elapse}')
            time.sleep(1)
            print(f'after time.sleep(1) twice, t.elapse = {t.elapse}')
        print(f'after with, t.elapse = {t.elapse}')

        test: Test = Test()
        test.say_something('Hello World!')

        self.assertEqual(2, add(1, 1))
        self.assertEqual(1, sub(2, 1))

    def test_info_level(self):
        t = get_timer(logging.WARNING)
        with t('warning test'):
            pass


if __name__ == '__main__':
    unittest.main()
