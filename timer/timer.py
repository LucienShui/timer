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
            self._func = name_or_func
            self._name = None
        else:
            self._func = None
            self._name: str = name_or_func

        self._unit: str = unit

        self._logger: logging.Logger = logging.getLogger('timer')

        self._begin: float = ...
        self._end: float = ...
        self._elapse: float = ...

    @property
    def elapse(self) -> float:
        if self._elapse is ...:
            return perf_counter() - self._begin
        return self._elapse

    def _start(self):
        self._begin = perf_counter()

    def _stop(self, name: str) -> None:
        self._end = perf_counter()
        self._elapse: float = self._end - self._begin

        logger = self._logger.getChild(name)

        if self._unit == 'ms' or (self._unit == 'auto' and self._elapse < 1):
            logger.debug(f'{self._elapse * 1000: .0f} ms')
        else:
            logger.debug(f'{self._elapse: .3f} s')

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop('timer' if self._name is None else self._name)

    def __call__(self, *args, **kwargs):

        if self._func is None:
            func = args[0]

            def wrapper(*_args, **_kwargs):
                self._start()
                _result = func(*_args, **_kwargs)
                self._stop(func.__name__ if self._name is None else self._name)
                return _result

            return wrapper
        else:
            self._start()
            result = self._func(*args, **kwargs)
            self._stop(self._func.__name__ if self._name is None else self._name)
            return result
