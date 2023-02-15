import pytest
from pytest_mock import mocker
import requests
import pandas as pd
from bs4 import BeautifulSoup

from dawson_college_pyscrapper.constants import DEFAULT_HEADERS
from dawson_college_pyscrapper.exceptions import PageDetailsError
from dawson_college_pyscrapper.util import get_date_of_modification, get_number_of_type, get_soup_of_page, parse_program_page


@pytest.fixture
def mock_successful_response():
    class Response:
        def __init__(self):
            self.ok = True
            self.text = '<html><body><p class="page-mod-date">Last Modified: 01-01-2022</p></body></html>'
            self.status_code = 200

    return Response()


@pytest.fixture
def mock_successful_response_no_content():
    class Response:
        def __init__(self):
            self.ok = True
            self.text = "<html><body></body></html>"
            self.status_code = 200

    return Response()


@pytest.fixture
def mock_failed_response():
    class Response:
        def __init__(self):
            self.ok = False
            self.text = ""
            self.status_code = 404

    return Response()


def test_get_soup_of_page(mocker, mock_successful_response):
    mocker.patch("requests.get").return_value = mock_successful_response
    url = "https://www.dawsoncollege.qc.ca/programs"
    soup = get_soup_of_page(url)
    assert (
        soup.prettify().strip() == '<html>\n <body>\n  <p class="page-mod-date">\n   Last Modified: 01-01-2022\n  </p>\n </body>\n</html>'
    )


def test_get_soup_of_page_not_ok(mocker, mock_failed_response):
    mocker.patch("requests.get").return_value = mock_failed_response
    url = "https://www.dawsoncollege.qc.ca/programs"
    with pytest.raises(PageDetailsError):
        soup = get_soup_of_page(url)


def test_get_date_of_modification(mocker, mock_successful_response):
    mocker.patch("requests.get").return_value = mock_successful_response
    url = "https://www.dawsoncollege.qc.ca/programs"
    soup = get_soup_of_page(url)
    date_modified = get_date_of_modification(soup)
    assert date_modified == "01-01-2022"


def test_get_date_of_modification_not_found(mocker, mock_successful_response_no_content):
    mocker.patch("requests.get").return_value = mock_successful_response_no_content
    url = "https://www.dawsoncollege.qc.ca/programs"
    soup = get_soup_of_page(url)
    date_modified = get_date_of_modification(soup)
    assert date_modified == ""


def test_parse_program_page(mocker, mock_successful_response):
    mocker.patch("requests.get").return_value = mock_successful_response
    url = "https://www.dawsoncollege.qc.ca/programs/program-name"
    program_data = parse_program_page(url)
    assert program_data.date == "01-01-2022"


def test_get_number_of_type_zero(mocker):
    df = pd.DataFrame({"program_type": [1, 2, 3]})

    result = get_number_of_type(df, "test")
    assert result == 0


def test_get_number_of_type_some_types_found(mocker):
    df = pd.DataFrame({"program_type": ["test", "another test", "test"]})

    result = get_number_of_type(df, "test")
    assert result == 2
