import logging
import types
import typing
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


def get_timer(level: int = logging.DEBUG):
    class Timer(object):

        _level = level

        def __init__(self, name_or_func: typing.Any = None, unit: str = 'auto'):
            """
            :param name_or_func: name of function, or function itself, user should not care about this parameter
            :param unit: time's unit, should be one of 's', 'ms' or 'auto'
            """
            if unit not in ['s', 'ms', 'auto']:
                raise AssertionError(f"field unit should be one of 's', 'ms', 'auto', got {unit}")

            if isfunction(name_or_func):
                self._func = name_or_func
                self.__name__ = name_or_func.__name__
            else:
                self._func = None
                self.__name__ = name_or_func or "timer"

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

        def _start(self) -> None:
            logger = self._logger.getChild(self.__name__)
            _log(logger, self._level, 'start')
            self._begin = perf_counter()

        def _stop(self) -> None:
            self._end = perf_counter()
            self._elapse: float = self._end - self._begin

            logger = self._logger.getChild(self.__name__)

            if self._unit == 'ms' or (self._unit == 'auto' and self._elapse < 1):
                _log(logger, self._level, f'cost {self._elapse * 1000:.0f} ms')
            else:
                _log(logger, self._level, f'cost {self._elapse:.3f} s')

        def __enter__(self):
            self._start()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._stop()

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
                    self._start()
                    _result = func(*_args, **_kwargs)
                    self._stop()
                    return _result

                return wrapper
            else:
                self._start()
                result = self._func(*args, **kwargs)
                self._stop()
                return result

        @classmethod
        def set_level(cls, new_level: int):
            cls._level = new_level

    return Timer
