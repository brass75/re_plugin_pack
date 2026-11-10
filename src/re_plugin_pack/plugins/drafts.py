"""Plugin to enable skipping draft pages"""

from render_engine import Collection, Site
from render_engine.plugins import hook_impl


class Drafts:
    default_settings: dict[str, bool] = {'show_drafts': True}

    @staticmethod
    @hook_impl
    def pre_build_collection(collection: Collection, site: Site, settings: dict[str, dict[str, bool]]):
        """
        If enabled, skip pages with a draft attribute that is set to True

        :param collection: Collection object to run on
        :param site: Site object
        :param settings: Settings for the plugin
        """
        settings: dict[str, bool] = settings['Drafts']
        if settings['show_drafts']:
            print('Showing draft pages.')
            return
        collection.pages = [page for page in collection.sorted_pages if not getattr(page, 'draft', False)]
