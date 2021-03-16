from __future__ import absolute_import, print_function

import logging
import types
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

    def _start(self, name: str) -> None:
        logger = self._logger.getChild(name)
        logger.debug('start')
        self._begin = perf_counter()

    def _stop(self, name: str) -> None:
        self._end = perf_counter()
        self._elapse: float = self._end - self._begin

        logger = self._logger.getChild(name)

        if self._unit == 'ms' or (self._unit == 'auto' and self._elapse < 1):
            logger.debug(f'cost {self._elapse * 1000:.0f} ms')
        else:
            logger.debug(f'cost {self._elapse:.3f} s')

    def __enter__(self):
        self._start(self._name or 'timer')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop(self._name or 'timer')

    def __get__(self, instance, owner):
        """
        return object itself when decorate function of object
        (source code copied from web)
        :param instance: I don't know
        :param owner: I don't know
        :return: I don't know
        """
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):

        if self._func is None:
            func = args[0]

            def wrapper(*_args, **_kwargs):
                __name: str = self._name or func.__name__
                self._start(__name)
                _result = func(*_args, **_kwargs)
                self._stop(__name)
                return _result

            return wrapper
        else:
            name: str = self._name or self._func.__name__
            self._start(name)
            result = self._func(*args, **kwargs)
            self._stop(name)
            return result
