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

### Documentation

Functions and modules should always have docstrings which describe them. Function docstrings written in the [RestructedText](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html), [Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html), or [NumPy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy) styles are preferred.

Documentation can be published to our private [ReadTheDocs](https://readthedocs.com/organizations/newton-crypto/). Everything necessary
for automatic generation is included in new projects by default, new repos just need to be enabled on ReadTheDocs to start the process.

Sphinx is used to generate documentation. This README will be included, along with a reference section containing all functions, modules, and classes that can be auto-discovered. If `__all__` is set in a module's `__init__.py` file, only those functions, modules, or classes will be published in the docs. Properly formatted docstrings and parameter/variable typing will be parsed and linked automatically.

References to modules, classes, and functions can be embedded in this README by using the following syntax:

```
{mod}`module.submodule_name`
{func}`module.function_name`
{class}`module.ClassName`
```

### Pre-commit

A number of pre-commit hooks are set up to ensure all commits meet basic code quality standards.

If one of the hooks changes a file, you will need to `git add` that file and re-run `git commit` before being able to continue.

### Git Workflow

This repo is configured for trunk-based development. When adding a new fix or feature, create a new branch off of `main`.

Merges into main _must always be rebased and squashed_. This can be done manually or with GitHub's "Squash and Merge" feature.

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
