import tempfile
from pathlib import Path

import pytest
from render_engine import Collection, Page, Site

from re_plugin_pack import LatestEntries


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


class Page3(Page):
    content = title = 'page3'


class Page4(Page):
    content = title = 'page4'


class Page5(Page):
    content = title = 'page5'


SETTINGS_EXPECTED = [
    (
        {},
        {
            'COLLECTIONS': {
                'MyBlog': {
                    'entries': [
                        {'title': 'page1', 'url': '/.//page1.html'},
                        {'title': 'page2', 'url': '/.//page2.html'},
                        {'title': 'page3', 'url': '/.//page3.html'},
                    ],
                    'url': '/.//',
                }
            }
        },
    ),
    (
        {'max_entries': 1},
        {
            'COLLECTIONS': {
                'MyBlog': {
                    'entries': [
                        {'title': 'page1', 'url': '/.//page1.html'},
                    ],
                    'url': '/.//',
                }
            }
        },
    ),
    (
        {'MyBlog': 0},
        {'COLLECTIONS': {}},
    ),
    (
        {'MyBlog': -1},
        {
            'COLLECTIONS': {
                'MyBlog': {
                    'entries': [
                        {'title': 'page1', 'url': '/.//page1.html'},
                        {'title': 'page2', 'url': '/.//page2.html'},
                        {'title': 'page3', 'url': '/.//page3.html'},
                        {'title': 'page4', 'url': '/.//page4.html'},
                        {'title': 'page5', 'url': '/.//page5.html'},
                    ],
                    'url': '/.//',
                }
            }
        },
    ),
    (
        {
            'collection': ['url', 'slug'],
            'entries': ['title', 'url', 'slug'],
        },
        {
            'COLLECTIONS': {
                'MyBlog': {
                    'entries': [
                        {'slug': None, 'title': 'page1', 'url': '/.//page1.html'},
                        {'slug': None, 'title': 'page2', 'url': '/.//page2.html'},
                        {'slug': None, 'title': 'page3', 'url': '/.//page3.html'},
                    ],
                    'slug': 'myblog',
                    'url': '/.//',
                }
            }
        },
    ),
]


@pytest.mark.parametrize('settings, expected', SETTINGS_EXPECTED)
def test_site_level_registration(site, settings, expected):
    """Test plugin at the Site level"""
    if settings:
        site.register_plugins(LatestEntries, LatestEntries=settings)
    else:
        site.register_plugins(LatestEntries)

    @site.page
    class Index(Page):
        content = 'Test'

    @site.collection
    class MyBlog(Collection):
        pages = [Page1(), Page2(), Page3(), Page4(), Page5()]

    site.render()
    assert site.route_list['index'].template_vars == expected


@pytest.mark.parametrize('settings, expected', SETTINGS_EXPECTED)
def test_page_level_registration(site, settings, expected):
    """Test plugin at the Site level"""

    @site.page
    class Index(Page):
        plugins = [(LatestEntries, settings)] if settings else [LatestEntries]
        content = 'Test'

    @site.collection
    class MyBlog(Collection):
        pages = [Page1(), Page2(), Page3(), Page4(), Page5()]

    site.render()
    assert site.route_list['index'].template_vars == expected
