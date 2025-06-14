"""Plugin to add next & prev links to items in a collection"""

from render_engine import Collection, Site
from render_engine.plugins import hook_impl


class NextPrevPlugin:
    default_settings = {}

    @staticmethod
    @hook_impl
    def pre_build_collection(collection: Collection, site: Site, settings: dict):
        """
        Update a list of pages with links for the previous and next posts abd the URL for the Collection archive.

        Can be registered with the Site or one or more Collections.

        Note that if the sort is reversed for the collection (which is the default for Blog) you will
             want to have `reversed: true` for the settings of this plugin.

        Example implementation:
        {% if collection_url %}
            <hr/>
            <p style="text-align: center;">
            {% if prev_url %}
            Previous: <a href="{{ prev_url }}">{{ prev_title }}</a>&nbsp;&nbsp;&nbsp;&nbsp;
            {% endif %}
            {% if next_url %}
            &nbsp;&nbsp;&nbsp;&nbsp;Next: <a href="{{ next_url }}">{{ next_title }}</a>
            {% endif %}
            </p>
        {% endif %}

        :param collection: Collection instance
        :param site: Site object - not used but part of the prototype for this hook
        :param settings: Plugin settings
        """
        settings = settings['NextPrevPlugin']
        reverse = collection.sort_reverse
        pages = collection.sorted_pages[::-1] if reverse else collection.sorted_pages
        collection_url = collection.routes[0]
        max_page = len(pages) - 1
        for i, page in enumerate(pages):
            template_vars = dict()
            if i < max_page:
                template_vars['next_url'] = pages[i + 1].url_for()
                template_vars['next_title'] = pages[i + 1].title
                for attr in settings.get('additional_attributes', list()):
                    template_vars[f'next_{attr}'] = getattr(pages[i + 1], attr, None)
            if i > 0:
                template_vars['prev_url'] = pages[i - 1].url_for()
                template_vars['prev_title'] = pages[i - 1].title
                for attr in settings.get('additional_attributes', list()):
                    template_vars[f'prev_{attr}'] = getattr(pages[i - 1], attr, None)
            template_vars['collection_url'] = collection_url
            template_vars['collection_title'] = collection._title
            page.template_vars = template_vars
