#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `exceptions` package in dawson_college_pyscrapper."""

import pytest

from dawson_college_pyscrapper.exceptions import PageDetailsError


def test_PageDetailsError_exception():
    with pytest.raises(PageDetailsError) as exc_info:
        raise PageDetailsError()

    assert str(exc_info.value) == "Could not get page details."
