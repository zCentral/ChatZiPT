"""
ChatZiPT - A Python-based AI chat application.
"""

from .core import ChatZiPT, ConversationHistory
from .config import config

__version__ = "0.1.0"
__author__ = "zCentral"
__email__ = "eirestiffanyy@gmail.com"

__all__ = ["ChatZiPT", "ConversationHistory", "config"]