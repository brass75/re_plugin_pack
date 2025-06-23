import datetime
from typing import Any

from dateutil import parser as date_parser
from render_engine import Collection, Page, Site
from render_engine.plugins import hook_impl


class DateNormalizer:
    default_settings = {}

    @staticmethod
    @hook_impl
    def pre_build_site(
        site: Site,
        settings: dict[str, Any],
    ) -> None:
        """
        Normalize dates in pages to be datetime for proper functioning

        :param site: Site
        :param settings: Settings object
        :return: None
        """
        for entry in site.route_list.values():
            match entry:
                case Page():
                    DateNormalizer._handle_date(entry)
                case Collection():
                    for page in entry:
                        DateNormalizer._handle_date(page)

    @staticmethod
    def _handle_date(entry: Page) -> None:
        """
        Normalize the date attribute in a Page

        :return: None
        """
        if hasattr(entry, 'date'):
            match entry.date:
                case datetime.date():
                    entry.date = date_parser.parse(str(entry.date))
                case str():
                    entry.date = date_parser.parse(entry.date)
                case datetime.datetime():
                    pass
                case _:
                    raise AttributeError(f'Unknown date type: {type(entry.date)} {entry.date}')
