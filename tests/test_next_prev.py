import tempfile
from pathlib import Path

import pytest
from render_engine import Collection, Page, Site

from re_plugin_pack import NextPrevPlugin


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


def test_next_prev_plugin_no_additional(site):
    @site.collection
    class MyBlog(Collection):
        pages = [Page1(), Page2(), Page3(), Page4(), Page5()]
        plugins = [NextPrevPlugin]

    my_blog = site.route_list['myblog']
    my_blog._run_collection_plugins(site=site, hook_type='pre_build_collection')

    output = [page.template_vars for page in my_blog.sorted_pages]
    assert output == [
        {'collection_title': 'MyBlog', 'collection_url': './', 'next_title': 'page2', 'next_url': '/page2.html'},
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next_title': 'page3',
            'next_url': '/page3.html',
            'prev_title': 'page1',
            'prev_url': '/page1.html',
        },
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next_title': 'page4',
            'next_url': '/page4.html',
            'prev_title': 'page2',
            'prev_url': '/page2.html',
        },
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next_title': 'page5',
            'next_url': '/page5.html',
            'prev_title': 'page3',
            'prev_url': '/page3.html',
        },
        {'collection_title': 'MyBlog', 'collection_url': './', 'prev_title': 'page4', 'prev_url': '/page4.html'},
    ]


def test_next_prev_plugin_with_additional(site):
    @site.collection
    class MyBlog(Collection):
        pages = [Page1(), Page2(), Page3(), Page4(), Page5()]
        plugins = [(NextPrevPlugin, {'additional_attributes': ['_slug']})]

    my_blog = site.route_list['myblog']
    my_blog._run_collection_plugins(site=site, hook_type='pre_build_collection')

    output = [page.template_vars for page in my_blog.sorted_pages]
    assert output == [
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next__slug': 'page2',
            'next_title': 'page2',
            'next_url': '/page2.html',
        },
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next__slug': 'page3',
            'next_title': 'page3',
            'next_url': '/page3.html',
            'prev__slug': 'page1',
            'prev_title': 'page1',
            'prev_url': '/page1.html',
        },
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next__slug': 'page4',
            'next_title': 'page4',
            'next_url': '/page4.html',
            'prev__slug': 'page2',
            'prev_title': 'page2',
            'prev_url': '/page2.html',
        },
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'next__slug': 'page5',
            'next_title': 'page5',
            'next_url': '/page5.html',
            'prev__slug': 'page3',
            'prev_title': 'page3',
            'prev_url': '/page3.html',
        },
        {
            'collection_title': 'MyBlog',
            'collection_url': './',
            'prev__slug': 'page4',
            'prev_title': 'page4',
            'prev_url': '/page4.html',
        },
    ]
