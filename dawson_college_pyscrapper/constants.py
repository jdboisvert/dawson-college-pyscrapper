"""A module which contains all the constants used in the project."""

from typing import Dict, Final

PROGRAMS_LISTING_URL: Final[str] = "https://www.dawsoncollege.qc.ca/programs/alphabetical-listing"
MAIN_WEBSITE_URL: Final[str] = "https://www.dawsoncollege.qc.ca"

DEFAULT_HEADERS: Final[Dict[str, str]] = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "referrer": "https://google.com",
}
