# re-plugin-pack

This is a plugin pack for the `render-engine` static site generator. It currently includes the
following plugins:

- [`LatestEntries`](#latestentries)
- [`NextPrevPlugin`](#nextprevplugin)

## `LatestEntries`

This plugin will add a list of the latest entries for one or more `Collection`s to a given `Page`.
It can be configured at the Page or `Site` levels and can be configured to provide the latest entries
for any number of `Collection`s. The entries used are in the sort order as defined in the `Collection` 
object.

### Settings

The plugin has the following default settings:

```python
{
    "collection": ["url"],
    "entries": ["title", "url"],
    "pages": ["index"],
    "max_entries": 3,
}
```
- `collection` - a list of attributes to include for the collection.
- `entries` - a list of attributes to include for a given entry.
- `pages` - a list of pages to add the `COLLECTIONS` entry to it's `template_vars` (Only needed when running as a 
`Site` plugin)
- `max_entries` - The maximum number of entries to include for a collection. The default is 3. `-1` indicates 
that all entries should be populated. 

In addition to the default settings entries can be added for each `Collection` defining how many
entries it should include:

- Positive integer - Include up to the number specified entries. For example: `'Collection1': 5` 
will include the 5 latest entries in the `template_vars`.
- `0` - Exclude this collection. For example: `'Collection2': 0` will not include `Collection2` 
in the `template_vars`.
- Negative integer - Include all entries. For example: `'Collection3': -1` will include all
entries for `Collection3` in the `template_vars`

### `Page` level configuration

To configure at the `Page` level just include `(LatestEntris, <settings_dict)` in the `plugins` 
attribute when declaring the `Page`. If no settings overrides are needed, include `LatestEntries`
by itself in the `plugin` attribute.

Example:
```python
from render_engine import Site, Page
from re-plugin-pack import LatestEntries

app = Site()
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
    ...
```

### `Site` level configuration

To configure at the `Site` level call `app.register_plugins(LatestEntries, LatestEntries=<settings>)`
if settings overrides are being used. To configure without additional settings, call
`app.register_plugin(LatestEntries)`.

Example:
```python
from render_engine import Site, Page
from re-plugin-pack import LatestEntries

app = Site()

# The following will use the default settings overriding the pages to run on to be page1 and page2
app.register_plugins(LatestEntries, LatestEntries={'pages': ['page1', 'page2']})

# The following will only enable for the Blog collection:
app.register_plugins(LatestEntries, LatestEntries={'max_entries': 0, 'Blog': 3})
```

NOTE: If configuring at the `Site` level the registration should be done _after_ adding all 
`Page` entries to the `Site`. When adding a `Page` to a `Site` all plugins registered to the
`Site` are automatically registered to the new `Page` object.

### Including in the `Page` template

The latest entries will be added to the `COLLECTIONS` key of the `template_vars` for the `Page`
and can be accessed in the template as `COLLECTIONS`.

Example template implementation:
```
{% for collection, collection_data in COLLECTIONS.items() %}
    Most recent <a href="{{ collection_data['url'] }}">{{ collection }}</a> entries:
    <ul>
    {% for entry in collection_data['entries'] %}
        <li><a href="{{ entry['url'] }}">{{ entry['title'] }}</a></li>
    {% endfor %}
    </ul>
{% endfor %}
```

## `NextPrevPlugin`

This plugin will give each page in a `Collection` access to certain attributes of the next and 
previous pages in the collection. By default, only the URL and title of those pages will be
made available, however additional attributes may also be requested via the settings. If an
attributes is in the list to include but does not exist in the page(s) `None` will be used.
This plugin runs at the `Collection` level and can be registered at the `Site` or `Collection`
level.

### Settings

This plugin has no default settings. If you wish to add additional attributes, include in the
registration a settings dictionary with a key of `additional_attributes` having a list of 
attributes as its value.

### `Site` level configuration

To configure at the `Site` level call `app.register_plugins(NextPrevPlugin, NextPrevPlugin=<settings>)`
if settings overrides are being used. To configure without additional settings, call
`app.register_plugin(NextPrevPlugin)`.

Example:
```python
from render_engine import Site, Page
from re-plugin-pack import NextPrevPlugin

app = Site()

# The following will include the date attribute in in the data made available.
app.register_plugins(NextPrevPlugin, NextPrevPlugin={'additional_attributes': ['date']})

# The following will not include any additional attributes
app.register_plugins(NextPrevPlugin)
```

NOTE: If configuring at the `Site` level the registration should be done _after_ adding all 
`Collection` entries to the `Site`. When adding a `Collection` to a `Site` all plugins 
registered to the `Site` are automatically registered to the new `Collection` object.

### `Collection` level configuration

To configure at the `Page` level just include `(NextPrevPlugin, <settings_dict)` in the `plugins` 
attribute when declaring the `Collection`. If no settings overrides are needed, include
`NextPrevPlugin` by itself in the `plugin` attribute.

Example:
```python
from render_engine import Site, Page
from re-plugin-pack import NextPrevPlugin

app = Site()
@app.page
class MyPage(Page):
    plugins = [
        (
            NextPrevPlugin,
            {
                'additional_attributes': [  # This will make the date and description attributes available
                    'date',
                    'description',
                ]
            },
        )
    ]
    ...
```

### Including in the `Collection` template

When run this plugin will add a dictionary with the requested data to the `template_vars` of 
each page in the `Collection`. The dictionary added looks like:

```python
{
    'collection_url': <url>,
    'collection_title': <title>,
    'next_url': <url>,
    'next_title': <title>,
    'prev_url': <url>,
    'prev_title': <title>,
}
```

If `additional_attributes` are included in the settings, they will be in the dictionary as:
`prev_<attr>: <value>` and `next_<attr>: <value>`.

```
{% if prev_url %}
<span class="prev_data">
Previous: <a href="{{ prev_url }}">{{ prev_title }}</a>
</span>
{% endif %}
{% if next_url %}
<span class="next_data">
Next: <a href="{{ next_url }}">{{ next_title }}</a>
</span>
{% endif %}
```
