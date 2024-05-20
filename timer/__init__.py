import logging

from .__version__ import __version__, __version_info__
from .timer import get_timer

timer = get_timer(level=logging.DEBUG)
