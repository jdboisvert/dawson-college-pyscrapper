from datetime import datetime
import pytest
import requests
import requests_mock
from bs4 import BeautifulSoup
from freezegun import freeze_time
from dawson_college_pyscrapper.constants import MAIN_WEBSITE_URL, PROGRAMS_LISTING_URL
from dawson_college_pyscrapper.exceptions import PageDetailsError
from dawson_college_pyscrapper.models import GeneralMetrics, Program, ProgramPageData

from dawson_college_pyscrapper.scrapper import (
    get_program_details,
    get_programs,
    get_total_number_of_faculty,
    get_total_number_of_students,
    scrap,
)
from tests.utils import get_invalid_program_listing, get_valid_program_listing


@pytest.mark.parametrize(
    "program_url, listed_program, returned_date, expected",
    [
        (
            "https://www.dawsoncollege.qc.ca/programs/program-name",
            get_valid_program_listing(),
            "2023-01-01",
            Program(
                name="Program Name",
                modified_date="2023-01-01",
                program_type="Certificate",
                url="https://www.dawsoncollege.qc.ca/programs/program-name",
            ),
        ),
        ("https://www.dawsoncollege.qc.ca/programs/program-name", get_invalid_program_listing(), "2023-01-01", None),
    ],
)
def test_get_program_details(mocker, program_url, listed_program, returned_date, expected):
    mocker.patch("dawson_college_pyscrapper.scrapper.parse_program_page", return_value=ProgramPageData(date=returned_date))
    result = get_program_details(program_url, listed_program)
    assert result == expected


def test_get_programs_returns_list_of_programs(mocker, requests_mock):
    # Just mock this function to return a Program object with the given name and date since this function is tested above.
    mocked_program = Program(
        name="Program Name",
        modified_date="2023-01-01",
        program_type="Certificate",
        url="https://www.dawsoncollege.qc.ca/programs/program-name",
    )
    mocker.patch("dawson_college_pyscrapper.scrapper.get_program_details", return_value=mocked_program)

    example_html = """
    <html>
        <body>
            <div class="entry-content">
                <table>
                    <tbody>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/program-1">Program 1</a>
                            </td>
                            <td class="program-type">
                                Full-time
                            </td>
                        </tr>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/program-2">Program 2</a>
                            </td>
                            <td class="program-type">
                                Part-time
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    requests_mock.get(PROGRAMS_LISTING_URL, text=example_html)

    result = get_programs()

    # We expect two programs to be returned since there are two programs in the example html.
    expected_programs = [mocked_program, mocked_program]
    assert result == expected_programs


def test_get_programs_returns_empty_list_when_no_program_name_found(requests_mock):
    example_html = """
    <html>
        <body>
            <div class="entry-content">
                <table>
                    <tbody>
                        <tr>
                            <td class="program-type">
                                Full-time
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    requests_mock.get(PROGRAMS_LISTING_URL, text=example_html)

    result = get_programs()

    assert result == []


def test_get_programs_returns_empty_list_when_general_education_found(requests_mock):
    example_html = """
    <html>
        <body>
            <div class="entry-content">
                <table>
                    <tbody>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/general-education">General Education Fun</a>
                            </td>
                            <td class="program-type">
                                Full-time
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    requests_mock.get(PROGRAMS_LISTING_URL, text=example_html)

    result = get_programs()

    assert result == []


def test_get_programs_returns_empty_list_no_details(mocker, requests_mock):
    mocker.patch("dawson_college_pyscrapper.scrapper.get_program_details", return_value=None)
    example_html = """
    <html>
        <body>
            <div class="entry-content">
                <table>
                    <tbody>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/program-1">Program 1</a>
                            </td>
                            <td class="program-type">
                                Full-time
                            </td>
                        </tr>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/program-2">Program 2</a>
                            </td>
                            <td class="program-type">
                                Part-time
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    requests_mock.get(PROGRAMS_LISTING_URL, text=example_html)

    result = get_programs()

    assert result == []


def test_get_programs_returns_empty_list_when_error_occurs(mocker, requests_mock):
    # Just mock this function to return an exception
    mocker.patch("dawson_college_pyscrapper.scrapper.get_program_details", side_effect=PageDetailsError())
    example_html = """
    <html>
        <body>
            <div class="entry-content">
                <table>
                    <tbody>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/program-1">Program 1</a>
                            </td>
                            <td class="program-type">
                                Full-time
                            </td>
                        </tr>
                        <tr>
                            <td class="program-name">
                                <a href="/programs/program-2">Program 2</a>
                            </td>
                            <td class="program-type">
                                Part-time
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    requests_mock.get(PROGRAMS_LISTING_URL, text=example_html)

    result = get_programs()

    assert result == []


def test_get_total_number_of_students(requests_mock):
    # For the sake of the test just return a number in the html. The page has much more than this normally.
    example_html = """
    <html>
        <body>
            <div class="Z0LcW t2b5Cf">11,000</div>
        </body>
    </html>
    """
    requests_mock.get(
        "https://www.google.com/search?q=dawson+college+number+of+students&stick=H4sIAAAAAAAAAOPgE-LUz9U3MLTMKjbV0s8ot9JPzs_JSU0uyczP088vSk_My6xKBHGKrfJKc5NSixTy0xSKS0pTUvNKihexKqYklhfn5ymANaWnKmCqAQDR74rvYgAAAA&sa=X&ved=2ahUKEwjXvq6b97XjAhUaQ80KHTRfCb8Q6BMoADAgegQIGhAC&biw=1156&bih=754",
        text=example_html,
    )

    result = get_total_number_of_students()

    assert result == 11000


def test_get_total_number_of_students_invalid_number_in_html(requests_mock):
    # For the sake of the test just return a number in the html. The page has much more than this normally.
    example_html = """
    <html>
        <body>
            <div class="Z0LcW t2b5Cf">11,000.5</div>
        </body>
    </html>
    """
    requests_mock.get(
        "https://www.google.com/search?q=dawson+college+number+of+students&stick=H4sIAAAAAAAAAOPgE-LUz9U3MLTMKjbV0s8ot9JPzs_JSU0uyczP088vSk_My6xKBHGKrfJKc5NSixTy0xSKS0pTUvNKihexKqYklhfn5ymANaWnKmCqAQDR74rvYgAAAA&sa=X&ved=2ahUKEwjXvq6b97XjAhUaQ80KHTRfCb8Q6BMoADAgegQIGhAC&biw=1156&bih=754",
        text=example_html,
    )

    with pytest.raises(ValueError):
        get_total_number_of_students()


def test_get_total_number_of_students_unable_to_find_tag(requests_mock):
    # For the sake of the test just return a number in the html. The page has much more than this normally.
    example_html = """
    <html>
        <body>
        </body>
    </html>
    """
    requests_mock.get(
        "https://www.google.com/search?q=dawson+college+number+of+students&stick=H4sIAAAAAAAAAOPgE-LUz9U3MLTMKjbV0s8ot9JPzs_JSU0uyczP088vSk_My6xKBHGKrfJKc5NSixTy0xSKS0pTUvNKihexKqYklhfn5ymANaWnKmCqAQDR74rvYgAAAA&sa=X&ved=2ahUKEwjXvq6b97XjAhUaQ80KHTRfCb8Q6BMoADAgegQIGhAC&biw=1156&bih=754",
        text=example_html,
    )

    # Assert that this will raise a ValueError exception
    with pytest.raises(AttributeError):
        get_total_number_of_students()


def test_get_total_number_of_faculty(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "<html><body><b>10</b></body></html>"
    mock_response.status_code = 200
    mocker.patch.object(requests, "post", return_value=mock_response)

    result = get_total_number_of_faculty()
    assert result == 10

    mock_response.text = "<html><body><b>20</b></body></html>"
    result = get_total_number_of_faculty()
    assert result == 20


def test_get_total_number_of_faculty_with_invalid_html(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "<html><body></body></html>"
    mock_response.status_code = 200
    mocker.patch.object(requests, "post", return_value=mock_response)

    with pytest.raises(IndexError):
        get_total_number_of_faculty()


@freeze_time("2023-01-20")
def test_scrap_value_correctly(mocker, *mocks):
    mocked_program = [
        Program(
            name="Program Name",
            modified_date="2023-01-01",
            program_type="Certificate",
            url="https://www.dawsoncollege.qc.ca/programs/program-name",
        ),
        Program(
            name="Program Name 2",
            modified_date="2023-01-01",
            program_type="Certificate",
            url="https://www.dawsoncollege.qc.ca/programs/program-name-2",
        ),
    ]
    mocker.patch("dawson_college_pyscrapper.scrapper.get_total_number_of_students", return_value=1000)
    mocker.patch("dawson_college_pyscrapper.scrapper.get_total_number_of_faculty", return_value=100)
    mocker.patch("dawson_college_pyscrapper.scrapper.get_programs", return_value=mocked_program)
    mocker.patch("dawson_college_pyscrapper.scrapper.get_number_of_type", return_value=10)

    result = scrap()

    assert isinstance(result, GeneralMetrics)
    assert result.date == datetime.now()  # Should be frozen to 2023-01-20
    assert result.total_programs_offered == 2
    assert result.number_of_programs == 10
    assert result.number_of_profiles == 10
    assert result.number_of_disciplines == 10
    assert result.number_of_special_studies == 10
    assert result.number_of_general_studies == 10
    assert result.total_year_counts == {"2023": 2}
    assert result.programs == mocked_program
    assert result.number_of_students == 1000
    assert result.number_of_faculty == 100
