#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `models` package in dawson_college_pyscrapper."""

import pytest
from datetime import datetime
from typing import List

from dawson_college_pyscrapper.models import Program, GeneralMetrics, ProgramPageData


def test_Program_model():
    program = Program(
        name="Program Name",
        modified_date="January 01, 2021",
        program_type="Certificate",
        url="https://www.dawsoncollege.qc.ca/programs/program-name",
    )

    assert program.name == "Program Name"
    assert program.modified_date == "January 01, 2021"
    assert program.program_type == "Certificate"
    assert program.url == "https://www.dawsoncollege.qc.ca/programs/program-name"


def test_GeneralMetrics_model():
    programs = [
        Program(
            name="Program 1",
            modified_date="January 01, 2021",
            program_type="Certificate",
            url="https://www.dawsoncollege.qc.ca/programs/program-1",
        ),
        Program(
            name="Program 2",
            modified_date="January 01, 2021",
            program_type="Diploma",
            url="https://www.dawsoncollege.qc.ca/programs/program-2",
        ),
    ]

    now = datetime.now()
    metrics = GeneralMetrics(
        date=now,
        total_programs_offered=2,
        number_of_programs=2,
        number_of_profiles=100,
        number_of_disciplines=50,
        number_of_special_studies=20,
        number_of_general_studies=30,
        number_of_students=1000,
        number_of_faculty=50,
        total_year_counts={2021: 2},
        programs=programs,
    )

    assert metrics.date == now
    assert metrics.total_programs_offered == 2
    assert metrics.number_of_programs == 2
    assert metrics.number_of_profiles == 100
    assert metrics.number_of_disciplines == 50
    assert metrics.number_of_special_studies == 20
    assert metrics.number_of_general_studies == 30
    assert metrics.number_of_students == 1000
    assert metrics.number_of_faculty == 50
    assert metrics.total_year_counts == {2021: 2}
    assert metrics.programs == programs

    assert metrics.number_of_students_per_faculty == 20.0

    sorted_programs = metrics.programs_sorted
    assert sorted_programs[0].name == "Program 1"
    assert sorted_programs[1].name == "Program 2"


def test_post_init_converts_programs_to_Program_objects_in_post_init():
    programs_data = [
        {
            "name": "Program 1",
            "modified_date": "January 01, 2021",
            "program_type": "Program",
            "url": "https://www.dawsoncollege.qc.ca/programs/program-1",
        },
        {
            "name": "Program 2",
            "modified_date": "January 01, 2021",
            "program_type": "Program",
            "url": "https://www.dawsoncollege.qc.ca/programs/program-2",
        },
    ]
    general_metrics = GeneralMetrics(
        date=datetime.now(),
        total_programs_offered=2,
        number_of_programs=2,
        number_of_profiles=0,
        number_of_disciplines=0,
        number_of_special_studies=0,
        number_of_general_studies=0,
        number_of_students=0,
        number_of_faculty=0,
        total_year_counts={},
        programs=programs_data,
    )

    assert all(isinstance(program, Program) for program in general_metrics.programs)


def test_ProgramPageData_model():
    data = ProgramPageData(date="January 01, 2021")

    assert data.date == "January 01, 2021"
