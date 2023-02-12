import os
import re
import sys

from sphinx_pyproject import SphinxConfig

sys.path.insert(0, os.path.abspath(".."))

config = SphinxConfig("../pyproject.toml", globalns=globals())

project = "dawson_college_pyscrapper"


github_url = "https://github.com/{github_username}/{github_repository}".format_map(config)

release = version = config.version

todo_include_todos = bool(os.environ.get("SHOW_TODOS", 0))

html_context = {
    "display_github": True,
    "github_user": config["github_username"],
    "github_repo": config["github_repository"],
    "github_version": "main",
    "conf_py_path": "/docs/",
}

toctree_plus_types = set(config["toctree_plus_types"])
