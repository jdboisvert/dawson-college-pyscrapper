"""A module which contains utils used by the scrapper for Dawson College."""

from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
import logging

from pandas import DataFrame

from dawson_college_pyscrapper.constants import DEFAULT_HEADERS
from dawson_college_pyscrapper.exceptions import PageDetailsError
from dawson_college_pyscrapper.models import ProgramPageData

logger = logging.getLogger(__name__)


def get_soup_of_page(url: str, header: Optional[Dict[str, str]] = None) -> BeautifulSoup:
    """
    Gets the BeautifulSoup object of the page at the given URL.

    :param url: The URL of the page to get the BeautifulSoup object of (ex: https://www.dawsoncollege.qc.ca/programs)
    :param header: The header to use when making the request. If not provided, the default header will be used.
    :return: The BeautifulSoup object of the page at the given URL.
    """
    header_to_use = header or DEFAULT_HEADERS

    response = requests.get(url, headers=header_to_use)

    if not response.ok:
        logger.debug(f"Failed to get the page at {url}. Got response code {response.status_code}")
        raise PageDetailsError

    return BeautifulSoup(response.text.strip(), "html.parser")


def get_date_of_modification(html_soup: BeautifulSoup) -> str:
    """
    Just a helper function to get the date of modification of the page.

    :param html_soup: The BeautifulSoup object of the page to get the date of modification of.
    :return: The date of modification of the page. If the date of modification is not found, an empty string will be returned.
    """
    default_return = ""
    if not (html_found := html_soup.find(class_="page-mod-date")):
        logger.debug(f"Failed to get the date of modification for {html_soup}")
        return default_return

    date_modified_text = html_found.contents[0].strip()

    return date_modified_text.replace("Last Modified: ", default_return)


def parse_program_page(program_url: str) -> ProgramPageData:
    """
    A helper function to parse the program page url and return an expected data structure.

    :param program_url: The URL of the program page to parse (ex: https://www.dawsoncollege.qc.ca/programs/program-name)
    :return: A ProgramPageData from the given url.
    """
    html_soup = get_soup_of_page(program_url)
    date_modified = get_date_of_modification(html_soup=html_soup)

    return ProgramPageData(date=date_modified)


def get_number_of_type(data_frame: DataFrame, wanted_type: str):
    """
    A helper function to get the number of programs of a given type.

    :param data_frame: The DataFrame to get the number of programs of a given type from. It is important that the DataFrame has a column named "program_type".
    :param wanted_type: The type of program to get the number of.
    :return: The number of programs of the given type.
    """
    query = data_frame["program_type"] == wanted_type

    return len(data_frame[query])
