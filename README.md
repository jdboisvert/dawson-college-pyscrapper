# Dawson College PyScrapper v1.0.0

A Python module which contains useful functions to help scrap data from [Dawson College](https://www.dawsoncollege.qc.ca/) which is a CEGEP in Montreal Quebec Canada.

## Features

- Get information on all the programs offered by Dawson College (ex: Computer Science, Computer Engineering, etc.)
- Get an estimate of the total number of students enrolled
- Get the total number of faculty members
- Get the general metrics of Dawson College (ex: total number of programs offered, number of programs, number of profiles, number of disciplines, number of special studies, number of general studies, etc.)

## Usage

### Installation

    pip install git+ssh://git@github.com/jdboisvert/dawson-college-pyscrapper


### Using the core functionality

#### Getting program details for a specific program

```python
from dawson_college_pyscrapper.scrapper import get_program_details

program_url = "https://www.dawsoncollege.qc.ca/programs/program-name"
# Get the BeautifulSoup Tag object of the program that is listed on the programs page.
listed_program = BeautifulSoup(requests.get(PROGRAMS_LISTING_URL).text.strip(), "html.parser").find("tr")

# Get the details of the program at the given URL.
program_details = get_program_details(program_url=program_url, listed_program=listed_program)
print(program_details)
```

#### Get details of all programs
```python
from dawson_college_pyscrapper.scrapper import get_programs

programs = get_programs()
for program in programs:
    print(f"Program Name: {program.name}")
    print(f"Modified Date: {program.modified_date}")
    print(f"Program Type: {program.program_type}")
    print(f"Program URL: {program.url}")
    print("\n")
```

#### Get the total number of students enrolled
```python
from dawson_college_pyscrapper.scrapper import get_total_number_of_students

total_number_of_students = get_total_number_of_students()
print(f"Total number of students: {total_number_of_students}")
```

#### Get the total number of faculty members
```python
from dawson_college_pyscrapper.scrapper import get_total_number_of_faculty_members

total_number_of_faculty_members = get_total_number_of_faculty_members()
print(f"Total number of faculty members: {total_number_of_faculty_members}")
```

#### Get the general metrics of Dawson College
```python
from dawson_college_pyscrapper.scrapper import scrap

generalMetrics = scrap()
print(f"Total programs offered: {GeneralMetrics.total_programs_offered}")
print(f"Number of programs: {GeneralMetrics.number_of_programs}")
print(f"Number of profiles: {GeneralMetrics.number_of_profiles}")
print(f"Number of disciplines: {GeneralMetrics.number_of_disciplines}")
print(f"Number of special studies: {GeneralMetrics.number_of_special_studies}")
print(f"Number of general studies: {GeneralMetrics.number_of_General_studies}")
print("\n")
print("Year count:")
for year, count in GeneralMetrics.total_year_counts.items():
    print(f"{year}: {count}")

print("\n")
print("Programs:")
for program in GeneralMetrics.programs:
    print(f"Program Name: {program.name}")
    print(f"Modified Date: {program.modified_date}")
    print(f"Program Type: {program.program_type}")
    print(f"Program URL: {program.url}")
    print("\n")
```

#### More examples
Check out the examples in the tests directory.

## Development

### Getting started

```shell
# install pyenv (if necessary)
brew install pyenv pyenv-virtualenv
echo """
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
""" > ~/.zshrc
source ~/.zshrc

# create a virtualenv
pyenv install 3.11.1
pyenv virtualenv 3.11.1 dawson_college_pyscrapper
pyenv activate dawson_college_pyscrapper

# install dependencies
pip install -U pip
pip install -e ".[dev]"
```

### Pre-commit

A number of pre-commit hooks are set up to ensure all commits meet basic code quality standards.

If one of the hooks changes a file, you will need to `git add` that file and re-run `git commit` before being able to continue.

To Install:
    pre-commit install


### Testing

[pytest](https://docs.pytest.org/en/6.2.x/) and [tox](https://tox.wiki/) are used for testing. Tox is configured to try testing against both Python 3.8 and Python 3.9 if you have them available. If one is missing, Tox will skip it rather than fail out.

    # just the unit tests against your current python version
    pytest

    # just the unit tests with a matching prefix
    pytest -k test_some_function

    # full test suite and code coverage reporting
    tox

## Credits

- Jeffrey Boisvert ([jdboisvert](https://github.com/jdboisvert)) [info.jeffreyboisvert@gmail.com](mailto:info.jeffreyboisvert@gmail.com)
