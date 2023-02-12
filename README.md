# Dawson College PyScrapper v0.0.0

A Python module which contains useful functions to help scrap data from Dawson College which is a CEGEP in Montreal Quebec Canada.

## Features

- Highlights and core functionality.

## Usage

### Installation

    pip install git+ssh://git@github.com/jdboisvert/dawson-college-pyscrapper
    

### Getting started

What does a user need before they start using this module or service?

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
pyenv install 3.9.11
pyenv virtualenv 3.9.11 dawson_college_pyscrapper
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

### PRs and Releases

GitHub Actions is configured to perform unit tests against MacOS and Linux runners using both Python 3.8, 3.9, and 3.10 for all new PRs.

To prevent automatic uploads remove everything below it in tagged-release.yml and delete setup.cfg file

If your work to a GitHub issue, be sure to reference it in the PR body. You can use the `closes` shortcut. eg: `Closes #123`.

It will also check if the version has been bumped. To do that, use `bumpver update`. This will bump the version number everywhere and create a new commit.

It will also check if the version has been bumped. To do that, use `bump2version`:

    # "patch" bumps are for minor non-breaking changes, hotfixes,
    # documentation updates, new tests, etc.
    bump2version patch

    # "minor" bumps are for significant backwards-compatible changes
    bump2version minor

    # "major" bumps are for breaking changes
    bump2version major

After merging in a PR, GitHub Actions will package the module and create a new release for it on GitHub.

#### Beta and Production releases

When a new version is created, the default is to flag the release as a "beta". After the release has been thoroughly tested and is ready for production, a new PR can be created to release it.

These extra steps help ensure ensure everything gets a chance to be tested in staging and to enable automated deployments to production.

    git checkout -b release/v1.2.3
    bump2version release
    git commit -am 'release: v1.2.3'
    git push -u origin release/v1.2.3

## Credits

- Jeffrey Boisvert ([jdboisvert](https://github.com/jdboisvert)) [info.jeffreyboisvert@gmail.com](mailto:info.jeffreyboisvert@gmail.com)
