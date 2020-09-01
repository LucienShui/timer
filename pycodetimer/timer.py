from __future__ import absolute_import, print_function

import logging
from inspect import isfunction
from time import perf_counter


class Timer(object):
    def __init__(self, name=None, logger_level: int = logging.DEBUG, unit: str = 'auto'):
        if isfunction(name):
            self.func = name
            self.name = None
        else:
            self.name: str = name

        self.logger_level: int = logger_level
        self.unit: str = unit

        self.logger: logging.Logger = logging.getLogger('timer')
        self.logger.setLevel(logger_level)

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
        if isfunction(args[0]):
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
