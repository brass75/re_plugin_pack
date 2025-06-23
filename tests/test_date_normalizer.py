import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from render_engine import Collection, Page, Site

from re_plugin_pack import DateNormalizer


@pytest.fixture(scope='function')
def site():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'site'
        app = Site()
        app.output_path = temp_path / 'output'

        yield app


class Page1(Page):
    content = title = 'page1'
    date = '2025-06-23'


class Page2(Page):
    content = title = 'page2'
    date = datetime.now()


class Page3(Page):
    content = title = 'page3'
    date = datetime.today().date()


class Page4(Page):
    content = title = 'page4'
    date = 1


class Page5(Page):
    content = title = 'page5'


def test_date_normalizer(site):
    """Test the DateNormalizer plugin with valid dates"""
    site.register_plugins(DateNormalizer)
    site.page(Page1)

    @site.collection
    class MyCollection(Collection):
        pages = [Page1(), Page2()]

    site.render()
    for entry in site.route_list.values():
        if isinstance(entry, Page):
            assert not hasattr(entry, 'date') or isinstance(entry.date, datetime)


def test_date_normalizer_invalid_date(site):
    """Test that AttributeError is thrown for an invalid date"""
    site.register_plugins(DateNormalizer)

    site.page(Page4)

    with pytest.raises(AttributeError):
        site.render()
