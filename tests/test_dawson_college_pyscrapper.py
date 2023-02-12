#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dawson_college_pyscrapper` package."""

import pytest

from dawson_college_pyscrapper import backend


def test_backend():
    """Sample pytest test function with the pytest fixture as an argument."""
    assert backend() == 4
