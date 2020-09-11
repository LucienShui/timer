from __future__ import absolute_import, print_function

import logging
import typing
from inspect import isfunction
from time import perf_counter


class Timer(object):

    def __init__(self, name_or_func: typing.Any = None, unit: str = 'auto'):
        """
        :param name_or_func: name of function, or function itself, user should not care about this parameter
        :param unit: time's unit, should be one of 's', 'ms' or 'auto'
        """
        if unit not in ['s', 'ms', 'auto']:
            raise AssertionError(f"field unit should be one of 's', 'ms', 'auto', got {unit}")

        if isfunction(name_or_func):
            self.func = name_or_func
            self.name = None
        else:
            self.func = None
            self.name: str = name_or_func

        self.unit: str = unit

        self.logger: logging.Logger = logging.getLogger('timer')

        self.begin: float = ...
        self.end: float = ...
        self.elapse: float = ...

    def start(self):
        self.begin = perf_counter()

    def stop(self, name: str) -> None:
        self.end = perf_counter()
        self.elapse: float = self.end - self.begin

        logger = self.logger.getChild(name)

        if self.unit == 'ms' or (self.unit == 'auto' and self.elapse < 1):
            logger.debug(f'{self.elapse * 1000: .0f} ms')
        else:
            logger.debug(f'{self.elapse: .3f} s')

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop('timer' if self.name is None else self.name)

    def __call__(self, *args, **kwargs):

        if self.func is None:
            func = args[0]

            def wrapper(*_args, **_kwargs):
                self.__enter__()
                _result = func(*_args, **_kwargs)
                self.stop(func.__name__ if self.name is None else self.name)
                return _result

            return wrapper
        else:
            self.__enter__()
            result = self.func(*args, **kwargs)
            self.stop(self.func.__name__ if self.name is None else self.name)
            return result
