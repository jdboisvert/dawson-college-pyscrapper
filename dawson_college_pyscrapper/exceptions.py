"""A module which contains custom exceptions used by the module."""


class PageDetailsError(Exception):
    """An exception which is used to indicate that the page details could not be retrieved."""

    def __str__(self) -> str:
        """
        A string representation of the exception.

        :return: A string representation of the exception.
        """
        return "Could not get page details."
