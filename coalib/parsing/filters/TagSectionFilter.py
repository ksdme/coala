def tag_section_filter(section, args):
    """
    Filters the sections by ``tags``. ``cli`` is always accepted.

    :param section: Section object.
    :param args:    Set of tags on which ``section`` is to be filtered.
    :return:        ``True`` if this section matches the criteria inside args,
                    ``False`` otherwise.
    """
    if section.name == 'cli':
        return True

    all_tags = args[0]
    enabled_tags = map(str.lower, all_tags)

    section_tags = section.get('tags', False)
    if str(section_tags) == 'False':
        return False

    section_tags = map(str.lower, section_tags)
    return bool(set(section_tags) & set(enabled_tags))
