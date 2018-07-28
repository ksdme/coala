def tag_filter(section, args):
    """
    Filters the sections by ``tags``. ``cli`` is always accepted.

    :param bear: Section object.
    :param args: Set of tags on which ``section`` is to be filtered.
    :return:     ``True`` if this section matches the criteria inside args,
                 ``False`` otherwise.
    """
    enabled_for_tags = map(str.lower, args[0])
    tags = map(str.lower, section.contents.get('tags', []))

    return bool(set(tags) & set(enabled_for_tags)) or section.name == 'cli'
