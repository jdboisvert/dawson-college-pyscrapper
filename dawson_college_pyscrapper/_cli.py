"""Console script for Dawson College PyScrapper."""
import sys
from typing import Dict

import click
from dawson_college_pyscrapper import backend


@click.command()
def main(args: Dict=None) -> int:
    """Console script for dawson_college_pyscrapper."""
    click.echo("Replace this message by putting your code into "
               "dawson_college_pyscrapper._cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
