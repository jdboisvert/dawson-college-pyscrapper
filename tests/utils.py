from bs4 import BeautifulSoup, Tag


def get_valid_program_listing() -> Tag:
    """
    Used to to create a valid program listing tag for testing purposes.

    :return: A valid program listing tag
    """
    mock_valid_html_content = """
    <div class="program-listing">
    <div class="program-type">Certificate</div>
    <div class="program-name">
        <a href="https://www.dawsoncollege.qc.ca/programs/program-name">Program Name</a>
    </div>
    </div>
    """

    soup = BeautifulSoup(mock_valid_html_content, "html.parser")
    valid_tag = soup.find(class_="program-listing")

    return valid_tag


def get_invalid_program_listing() -> Tag:
    """
    Used to to create an invalid program listing tag for testing purposes.

    :return: An invalid program listing tag
    """
    mock_invalid_html_content = """
    <div class="program-listing">
    <div class="program-name">
        <a href="https://www.dawsoncollege.qc.ca/programs/program-name">Program Name</a>
    </div>
    </div>
    """
    soup = BeautifulSoup(mock_invalid_html_content, "html.parser")
    invalid_tag = soup.find(class_="program-listing")

    return invalid_tag


def get_invalid_program_listing_empty() -> Tag:
    """
    Used to to create an invalid program listing tag for testing purposes (program-type is empty)

    :return: An invalid program listing tag
    """
    mock_invalid_html_content = """
    <div class="program-listing">
    <div class="program-type"></div>
    <div class="program-name">
        <a href="https://www.dawsoncollege.qc.ca/programs/program-name">Program Name</a>
    </div>
    </div>
    """
    soup = BeautifulSoup(mock_invalid_html_content, "html.parser")
    invalid_tag = soup.find(class_="program-listing")

    return invalid_tag
