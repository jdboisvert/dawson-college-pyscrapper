# Dawson College PyScrapper v0.0.0

A Python module which contains useful functions to help scrap data from [Dawson College](https://www.dawsoncollege.qc.ca/) which is a CEGEP in Montreal Quebec Canada.

## Features

- Get information on all the programs offered by Dawson College (ex: Computer Science, Computer Engineering, etc.)
- Get an estimate of the total number of students enrolled
- Get the total number of faculty members


## Usage

### Installation

    pip install git+ssh://git@github.com/jdboisvert/dawson-college-pyscrapper


### Using the core functionality

How should the user interact with this module or service?

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
