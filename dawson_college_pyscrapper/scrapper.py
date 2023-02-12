"""This module contains the scrapper for Dawson College."""

from datetime import datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import logging

from dawson_college_pyscrapper.constants import PROGRAMS_LISTING_URL, MAIN_WEBSITE_URL, DEFAULT_HEADERS
from dawson_college_pyscrapper.exceptions import PageDetailsError
from dawson_college_pyscrapper.models import Program, GeneralMetrics, ProgramPageData
from dawson_college_pyscrapper.util import get_number_of_type, get_soup_of_page, parse_program_page


logger = logging.getLogger(__name__)


def get_program_details(program_url: str, listed_program: Tag) -> Optional[Program]:
    """
    Gets the details of the program at the given URL.
    
    :param program_url: The URL of the program to get the details of (ex: https://www.dawsoncollege.qc.ca/programs/program-name)
    :param listed_program: The BeautifulSoup Tag object of the program that is listed on the programs page.
    :return: A Program object with the details of the program at the given URL. If the program is not a valid program, None will be returned.
    """
    if not (program_type := listed_program.find(class_="program-type")):
        logger.debug(f"Failed to get the program type for {program_url}, and listed_program: {listed_program}")
        return None
    
    program_type_data = program_type.contents[0].strip()
    program_name = (
        listed_program.find(class_="program-name").find("a").contents[0].strip()
    )
    program_page_data  = parse_program_page(program_url=program_url)

    return Program(
        name=program_name,
        modified_date=program_page_data.date,
        program_type=program_type_data,
        url=program_url,
    )
        
def get_programs() -> List[Program]:
    """
    Gets a list of all the programs listed on the programs page.
    
    :return: A list of all the programs listed on the programs page. If not programs are found it will return an empty list.
    """
    all_programs_listed_html_soup = get_soup_of_page(PROGRAMS_LISTING_URL)

    entry_content = all_programs_listed_html_soup.find(class_="entry-content")
    listed_programs = entry_content.find_all("tr")

    programs = []
    for listed_program in listed_programs:
        if not (program_name:= listed_program.find(class_="program-name")):
            logger.debug("Skipping since program name is not present.")
            continue

        program_path = program_name.find("a")["href"]
        if program_path == "/programs/general-education":
            logger.debug("Skipping since program path is a general education path.")
            continue

        program_url = f"{MAIN_WEBSITE_URL}/{program_path}"
        try:
            if program_details := get_program_details(program_url=program_url, listed_program=listed_program):
                # Only add the program if it is a valid program and can be found. If None it will never be added.
                programs.append(program_details)
                
        except PageDetailsError:
            logger.error(f"Error occurred while get details from {program_url}")
            continue

    return programs

def get_total_number_of_students() -> int:
    """
    Gets the total number of students at Dawson College (this is mainly an estimate).
    
    :return: The total number of students at Dawson College.
    :raises: ValueError if the number of students cannot be parsed to an int.
    :raises AttributeError: If the content containing the number of students cannot be found.
    """
    
    # TODO should use something more reliable than google here.
    soup = get_soup_of_page(
        "https://www.google.com/search?q=dawson+college+number+of+students&stick=H4sIAAAAAAAAAOPgE-LUz9U3MLTMKjbV0s8ot9JPzs_JSU0uyczP088vSk_My6xKBHGKrfJKc5NSixTy0xSKS0pTUvNKihexKqYklhfn5ymANaWnKmCqAQDR74rvYgAAAA&sa=X&ved=2ahUKEwjXvq6b97XjAhUaQ80KHTRfCb8Q6BMoADAgegQIGhAC&biw=1156&bih=754"
    )

    tag = soup.find(class_="Z0LcW")
    content = tag.contents[0].strip()

    return int(content.replace(",", ""))

def get_total_number_of_faculty() -> int:
    """
    Gets the total number of faculty at Dawson College.
    
    :return: The total number of faculty at Dawson College.
    """
    
    params = {"position": "Faculty", "search": "Search"}

    # This is needed to allow the post to go through.
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 "
        "Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = requests.post(
        f"{MAIN_WEBSITE_URL}/phone-directory", data=params, headers=headers
    )
    response_soup = BeautifulSoup(response.text, "html.parser")

    tags = response_soup.find_all("b")

    return int(tags[0].contents[0])

def scrap() -> GeneralMetrics:
    """
    This is a general purpose scrap method which will scrap all the data from the website and return it as a GeneralMetrics object.
    This is mainly a wrapper of the other methods offered and some nice to have metrics. 
    
    :return: A GeneralMetrics object with all the data scrapped from the website.
    """
    
    number_of_students = get_total_number_of_students()
    number_of_faculty = get_total_number_of_faculty()

    programs = get_programs()
    programs_data_frame = pd.DataFrame(programs)

    # Change date to actual Timestamp type
    programs_data_frame["date"] = pd.to_datetime(
        programs_data_frame["modified_date"]
    )

    total_programs_offered = len(programs_data_frame)
    number_of_programs = get_number_of_type(programs_data_frame, "Program")
    number_of_profiles = get_number_of_type(programs_data_frame, "Profile")
    number_of_disciplines = get_number_of_type(
        programs_data_frame, "Discipline"
    )
    number_of_special_studies = get_number_of_type(
        programs_data_frame, "Special Area of Study"
    )
    number_of_general_education = get_number_of_type(
        programs_data_frame, "General Education"
    )

    years = []
    for date in programs_data_frame["date"]:
        years.append(str(date.year))

    programs_data_frame["year"] = years
    total_year_counts = programs_data_frame["year"].value_counts()
    
    
    return GeneralMetrics(
        date=datetime.now(),
        total_programs_offered=total_programs_offered,
        number_of_programs=number_of_programs,
        number_of_profiles=number_of_profiles,
        number_of_disciplines=number_of_disciplines,
        number_of_special_studies=number_of_special_studies,
        number_of_general_studies=number_of_general_education,
        total_year_counts=total_year_counts.to_dict(),
        programs=programs,
        number_of_students=number_of_students,
        number_of_faculty=number_of_faculty,
    )