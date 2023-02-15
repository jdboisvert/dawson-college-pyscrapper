from datetime import datetime
import pytest
import requests
import requests_mock
from freezegun import freeze_time
from dawson_college_pyscrapper.constants import PROGRAMS_LISTING_URL
from dawson_college_pyscrapper.exceptions import PageDetailsError
from dawson_college_pyscrapper.models import GeneralMetrics, Program, ProgramPageData

from dawson_college_pyscrapper.scrapper import (
    get_program_details,
    get_programs,
    get_total_number_of_faculty,
    get_total_number_of_students,
    scrape,
)
from tests.utils import get_invalid_program_listing, get_invalid_program_listing_empty, get_valid_program_listing


@pytest.mark.parametrize(
    "program_url, listed_program, returned_date, expected",
    [
        (
            "https://www.dawsoncollege.qc.ca/programs/program-name",
            get_valid_program_listing(),
            "January 1, 2023",
            Program(
                name="Program Name",
                modified_date="January 1, 2023",
                program_type="Certificate",
                url="https://www.dawsoncollege.qc.ca/programs/program-name",
            ),
        ),
        ("https://www.dawsoncollege.qc.ca/programs/program-name", get_invalid_program_listing(), "January 1, 2023", None),
        ("https://www.dawsoncollege.qc.ca/programs/program-name", get_invalid_program_listing_empty(), None, None),
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
        modified_date="January 1, 2023",
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


def test_get_total_number_of_students(mocker):
    # For the sake of the test just return a number in the html. The page has much more than this normally.
    example_html = """
    <html>
        <body>
            <div class="BNeawe">Collège Dawson (French)</div>
            <div class="BNeawe">Collège Dawson (French)</div>
            <div class="BNeawe">Students</div>
            <div class="BNeawe">Dawson College (English)</div>
            <div class="BNeawe">11,000</div>
        </body>
    </html>
    """
    mock_response = mocker.Mock()
    mock_response.text = example_html
    mocker.patch.object(requests, "get", return_value=mock_response)

    result = get_total_number_of_students()

    assert result == 11000


def test_get_total_number_of_students_invalid_number_in_html(requests_mock):
    # For the sake of the test just return a number in the html. The page has much more than this normally.
    example_html = """
    <html>
        <body>
            <div class="BNeawe">Collège Dawson (French)</div>
            <div class="BNeawe">Collège Dawson (French)</div>
            <div class="BNeawe">Students</div>
            <div class="BNeawe">Dawson College (English)</div>
            <div class="BNeawe">11,000.5</div>
        </body>
    </html>
    """
    url = "https://www.google.ca/search?q=How+Many+Students+does+Dawson+College+have%3F&sxsrf=AJOqlzXG6QAv21OAKIauoknY8WvZK09WdQ%3A1676260186748&ei=WrPpY8CoLbar5NoP7aaTkA4&ved=0ahUKEwjAve3ny5H9AhW2FVkFHW3TBOIQ4dUDCA8&uact=5&oq=How+Many+Students+does+Dawson+College+have%3F&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAEyBQghEKABMgUIIRCgATIFCCEQoAEyBQghEKABOgoIABBHENYEELADOgQIIxAnOgUIABCRAjoLCAAQgAQQsQMQgwE6CwguEIMBELEDEIAEOhEILhCABBCxAxCDARDHARDRAzoOCC4QxwEQsQMQ0QMQgAQ6CAgAELEDEIMBOg4ILhCABBCxAxDHARDRAzoICAAQgAQQsQM6BQgAEIAEOgsILhCABBCxAxCDAToFCC4QgAQ6BwgAEIAEEAo6BwguEIAEEAo6BQgAELEDOgoIABCABBBGEPsBOgkIABAWEB4Q8QQ6BQgAEIYDOgsIIRAWEB4Q8QQQHToGCAAQHhANOgQIIRAVOgcIIRCgARAKSgQIQRgASgQIRhgAUL8HWNQ1YKk7aANwAXgAgAGMAYgB7xiSAQQzOS40mAEAoAEByAEIwAEB&sclient=gws-wiz-serp"
    requests_mock.get(
        url,
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
    url = "https://www.google.ca/search?q=How+Many+Students+does+Dawson+College+have%3F&sxsrf=AJOqlzXG6QAv21OAKIauoknY8WvZK09WdQ%3A1676260186748&ei=WrPpY8CoLbar5NoP7aaTkA4&ved=0ahUKEwjAve3ny5H9AhW2FVkFHW3TBOIQ4dUDCA8&uact=5&oq=How+Many+Students+does+Dawson+College+have%3F&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAEyBQghEKABMgUIIRCgATIFCCEQoAEyBQghEKABOgoIABBHENYEELADOgQIIxAnOgUIABCRAjoLCAAQgAQQsQMQgwE6CwguEIMBELEDEIAEOhEILhCABBCxAxCDARDHARDRAzoOCC4QxwEQsQMQ0QMQgAQ6CAgAELEDEIMBOg4ILhCABBCxAxDHARDRAzoICAAQgAQQsQM6BQgAEIAEOgsILhCABBCxAxCDAToFCC4QgAQ6BwgAEIAEEAo6BwguEIAEEAo6BQgAELEDOgoIABCABBBGEPsBOgkIABAWEB4Q8QQ6BQgAEIYDOgsIIRAWEB4Q8QQQHToGCAAQHhANOgQIIRAVOgcIIRCgARAKSgQIQRgASgQIRhgAUL8HWNQ1YKk7aANwAXgAgAGMAYgB7xiSAQQzOS40mAEAoAEByAEIwAEB&sclient=gws-wiz-serp"
    requests_mock.get(
        url,
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
            modified_date="January 20, 2023",
            program_type="Certificate",
            url="https://www.dawsoncollege.qc.ca/programs/program-name",
        ),
        Program(
            name="Program Name 2",
            modified_date="January 20, 2023",
            program_type="Certificate",
            url="https://www.dawsoncollege.qc.ca/programs/program-name-2",
        ),
    ]
    mocker.patch("dawson_college_pyscrapper.scrapper.get_total_number_of_students", return_value=1000)
    mocker.patch("dawson_college_pyscrapper.scrapper.get_total_number_of_faculty", return_value=100)
    mocker.patch("dawson_college_pyscrapper.scrapper.get_programs", return_value=mocked_program)
    mocker.patch("dawson_college_pyscrapper.scrapper.get_number_of_type", return_value=10)

    result = scrape()

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
