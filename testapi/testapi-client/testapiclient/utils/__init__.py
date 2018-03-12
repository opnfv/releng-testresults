def get_item_properties(item, fields):
    """Return a tuple containing the item properties.

    :param item: a single item resource (e.g. Server, Project, etc)
    :param fields: tuple of strings with the desired field names
    """

    return tuple([item.get(field, '') for field in fields])
