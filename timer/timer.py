import logging
from typing import Any, Callable
import types
from inspect import isfunction
from time import perf_counter


def _log(logger: logging.Logger, level: int, message: str):
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)
    else:
        raise AssertionError('wrong level')


def _get_logger_print_fn(logger: logging.Logger, level: int) -> Callable[[str], None]:
    if level == logging.DEBUG:
        return logger.debug
    if level == logging.INFO:
        return logger.info
    if level == logging.WARNING:
        return logger.warning
    if level == logging.ERROR:
        return logger.error
    if level == logging.CRITICAL:
        return logger.critical
    raise AssertionError('wrong level')


def get_timer(level: int = None, print_fn: Callable[[str], None] = None):
    class Timer(object):

        _level = level
        _print_fn = print_fn

        def __init__(self, name_or_func: Any = None, unit: str = 'auto'):
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

        def _log(self, message: str, name: str = None) -> None:
            if self._print_fn is not None:
                pass
            if self._level is not None:
                if name is not None:
                    _log(self._logger.getChild(name), self._level, message)

        @property
        def elapse(self) -> int:
            if self._end is ...:
                end = perf_counter()
            else:
                end = self._end
            return round((end - self._begin) * 1000)

        def _start(self, name: str) -> None:
            self._log('start', name=name)
            self._begin = perf_counter()

        def _stop(self, name: str) -> None:
            self._end = perf_counter()
            if self._unit == 'ms' or (self._unit == 'auto' and self.elapse < 1000):
                self._log(f'cost {self.elapse} ms', name=name)
            else:
                self._log(f'cost {self.elapse / 1000:.3f} s', name=name)

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

        @classmethod
        def set_level(cls, new_level: int):
            cls._level = new_level

    return Timer
