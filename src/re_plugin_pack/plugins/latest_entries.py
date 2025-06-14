"""Plugin for giving the latest entries"""

from render_engine import Collection, Page, Site
from render_engine.plugins import hook_impl


class LatestEntries:
    """
    Adds a dictionary to the index page's template_vars:

    default_settings = {
        "collection": ["url"],
        "entries": ["title", "url"],
        "pages": ["index"],
        "max_entries": 3,
    }

    To override the default number of entries add to the registration:
    {<collection title>: <max entries>}
    To disable set max entries to 0 for that collection
    To print all entries for a given collection set max entries to a negative number

    Can be registered on the Site object:
    app.register_plugins(LatestEntries, LatestEntries=<settings overrides>)

    Can be registered for an individual Page include it in the definition of the page:
    @app.page
    class MyPage(Page):
        plugins = [
            (
                LatestEntries,
                {
                    "Collection1": 5,  # Include the 5 most recent entries
                    "Collection2": 0,  # Exclude this collection
                    "Collection3": -1,  # Include all entries in the collection
                },
            )
        ]
    NOTE: If registering the plugin for an individual page the "page" part of the settings
          is irrelevant and not looked at. That settings is for when registering for the site.

    NOTE: "Most recent" is defined by the sort order for the given collection.
          The default for a Collection is "title" and the default for a Blog is date.
          You can override the sort order (which will affect the sorting for everything,
          just this plugin) by initializing the Collection object with the following attribute:
                sort_by = <sort attribute>

    To use put this into your index.html template or content:
    {% for collection, collection_data in COLLECTIONS.items() %}
        Most recent <a href="{{ collection_data['url'] }}">{{ collection }}</a> entries:
        <ul>
        {% for entry in collection_data['entries'] %}
            <li><a href="{{ entry['url'] }}">{{ entry['title'] }}</a></li>
        {% endfor %}
        </ul>
    {% endfor %}

    NOTE: Above example is using the default settings.
    """

    default_settings = {
        'collection': ['url'],
        'entries': ['title', 'url'],
        'pages': ['index'],
        'max_entries': 3,
    }

    @staticmethod
    @hook_impl
    def pre_build_site(site: Site, settings: dict):
        """
        Pre-build site hook

        :param site: Site object
        :param settings: Settings dictionary [Not currently used but required by the hook]
        """
        settings = settings['LatestEntries']
        pages = settings.get('pages', list())
        for page_entry in pages:
            page = site.route_list[page_entry]
            LatestEntries.build_latest_entries(site=site, page=page, settings=settings)

    @staticmethod
    @hook_impl
    def render_content(page: Page, settings: dict, site: Site):
        """
        Render content hook

        :param page: The page to update
        :param settings: The settings for the plugin
        :param site: The Site object.
        """
        LatestEntries.build_latest_entries(site, page, settings['LatestEntries'])

    @staticmethod
    def build_latest_entries(site: Site, page: Page, settings: dict):
        """
        Update the page with the latest entries.

        :param page: The page to update
        :param settings: The settings for the plugin
        :param site: The Site object.
        """
        collections = dict()
        for name, collection in site.route_list.items():
            if isinstance(collection, Collection):
                if not (max_entries := settings.get(collection.title, settings['max_entries'])):
                    continue
                if max_entries < 0:
                    max_entries = len(collection.sorted_pages)
                collections[collection.title] = {'entries': list()}
                for attr in settings['collection']:
                    if attr == 'url':
                        value = f'/{collection.routes[0]}/'
                    else:
                        value = getattr(collection, attr, None)
                    collections[collection.title][attr] = value
                for entry in collection.sorted_pages[:max_entries]:
                    entry_dict = dict()
                    for attr in settings['entries']:
                        if attr == 'url':
                            value = f'/{entry.routes[0]}/{entry._slug}.html'
                        else:
                            value = getattr(entry, attr, None)
                        entry_dict[attr] = value
                    collections[collection.title]['entries'].append(entry_dict)

        if not hasattr(page, 'template_vars'):
            page.template_vars = dict()
        if existing_collections := page.template_vars.get('COLLECTIONS'):
            existing_collections.update(collections)
        else:
            page.template_vars['COLLECTIONS'] = collections
