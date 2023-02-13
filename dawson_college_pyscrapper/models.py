"""Data models for Dawson College PyScrapper."""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class Program:
    """
    Represents a program at Dawson College.

    :param name: Name of the program.
    :param modified_date: Date when the program was last modified (ex: 2021-01-01).
    :param program_type: Type of the program (ex: Certificate, Diploma, etc.).
    :param url: URL of the program (ex: https://www.dawsoncollege.qc.ca/programs/program-name)
    """

    name: str
    modified_date: str
    program_type: str
    url: str


@dataclass(frozen=True)
class GeneralMetrics:
    """
    Represents the general metrics that are aggregated about Dawson College.

    :param date: Date when the metrics were pulled
    :param total_programs_offered: Total number of programs offered at Dawson College.
    :param number_of_programs: Number of programs offered at Dawson College.
    :param number_of_profiles: Number of profiles offered at Dawson College.
    :param number_of_disciplines: Number of disciplines offered at Dawson College.
    :param number_of_special_studies: Number of special studies offered at Dawson College.
    :param number_of_general_studies: Number of general studies offered at Dawson College.
    :param number_of_students: Number of students at Dawson College.
    :param number_of_faculty: Number of faculty at Dawson College.
    :param total_year_counts: Number of programs offered per year. This will be a dict object formatted as follows: {year: number_of_programs_offered}.
    :param programs: List of programs offered at Dawson College with additional details.
    """

    date: datetime
    total_programs_offered: int

    number_of_programs: int
    number_of_profiles: int
    number_of_disciplines: int
    number_of_special_studies: int
    number_of_general_studies: int
    number_of_students: int
    number_of_faculty: int

    total_year_counts: dict
    programs: List[Program]

    def __post_init__(self):
        """Ran after the __init__ method. This is used to convert the programs list to a list of Program objects."""
        for i in range(len(self.programs)):
            if not isinstance(self.programs[i], Program):
                self.programs[i] = Program(**{**self.programs[i]})

    @property
    def number_of_students_per_faculty(self) -> float:
        """
        Returns the number of students per faculty at Dawson College.

        :return: Number of students per faculty ratio at Dawson College rounded to 2 decimal places.
        """
        return round((self.number_of_students / self.number_of_faculty), 2)

    @property
    def programs_sorted(self) -> List[Program]:
        """
        Returns the list of programs sorted by the date they were last modified.

        :return: List of programs sorted by the date they were last modified.
        """
        return sorted(
            self.programs,
            key=lambda program: datetime.strptime(program.modified_date, "%B %d, %Y"),
            reverse=True,
        )


@dataclass(frozen=True)
class ProgramPageData:
    """
    A dataclass that represents the data that is scraped from a program page.

    :param date: Date when the page was modified (ex: 2021-01-01).
    """

    date: str
