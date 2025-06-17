import tempfile
from pathlib import Path

import pytest
from render_engine import Collection, Page, Site

from re_plugin_pack.plugins.drafts import Drafts


@pytest.fixture(scope='function')
def site():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'site'
        app = Site()
        app.output_path = temp_path / 'output'

        yield app


class Page1(Page):
    content = title = 'page1'


class Page2(Page):
    content = title = 'page2'
    draft = True


class Page3(Page):
    content = title = 'page3'
    draft = False


@pytest.mark.parametrize('show_drafts, expected', [(False, 2), (True, 3)])
def test_drafts(show_drafts, expected, site):
    """Tests that drafts are filtered properly"""

    @site.collection
    class MyCollection(Collection):
        pages = [Page1(), Page2(), Page3()]
        plugins = [(Drafts, {'show_drafts': show_drafts})]

    collection = site.route_list['mycollection']
    site.render()
    assert len(collection.pages) == expected
