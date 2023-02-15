# -*- coding: utf-8 -*-

"""Dawson College PyScrapper: A Python module which contains useful functions to help scrap data from Dawson College which is a CEGEP in Montreal Quebec Canada.."""

__author__ = """Jeffrey Boisvert"""
__email__ = "info.jeffreyboisvert@gmail.com"
__version__ = "1.1.1"

from . import models, scrapper, exceptions

# any functions from backend you want to expose should be
# imported above and added to the list below.
__all__ = [
    "models",
    "scrapper",
    "exceptions",
]
