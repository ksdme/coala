from coalib.parsing.InvalidFilterException import InvalidFilterException
from coalib.parsing.filters import available_filters, available_section_filters


def is_valid_filter(filter):
    return filter in available_filters


def is_valid_section_filter(filter):
    return filter in available_section_filters


def _filter_section_bears(bears, args, filter_name):
    filter_function = available_filters[filter_name]
    return {section:
            tuple(bear for bear in bears[section]
                  if filter_function(bear, args))
            for section in bears}


def apply_filter(filter_name, filter_args, all_bears=None):
    """
    Returns bears after filtering based on ``filter_args``. It returns
    all bears if nothing is present in ``filter_args``.

    :param filter_name:
        Name of the filter.
    :param filter_args:
        Arguments of the filter to be passed in.
        For example:
        ``['c', 'java']``
    :param all_bears:
        List of bears on which filter is to be applied.
        All the bears are loaded automatically by default.
    :return:
        Filtered bears based on a single filter.
    """
    if all_bears is None:
        from coalib.settings.ConfigurationGathering import (
            get_all_bears)
        all_bears = get_all_bears()
    if not is_valid_filter(filter_name):
        raise InvalidFilterException(filter_name)
    if not filter_args or len(filter_args) == 0:
        return all_bears

    filter_args = {arg.lower() for arg in filter_args}
    local_bears, global_bears = all_bears
    local_bears = _filter_section_bears(
        local_bears, filter_args, filter_name)
    global_bears = _filter_section_bears(
        global_bears, filter_args, filter_name)
    return local_bears, global_bears


def apply_filters(filters, bears=None):
    """
    Returns bears after filtering based on ``filters``. It returns
    intersection of bears if more than one element is present in ``filters``
    list.

    :param filters:
        List of args based on ``bears`` has to be filtered.
        For example:
        ``[['language', 'c', 'java'], ['can_fix', 'syntax']]``
    :param bears:
        The bears to filter.
    :return:
        Filtered bears.
    """
    for filter in filters:
        filter_name, *filter_args = filter
        bears = apply_filter(filter_name, filter_args, bears)
    return bears


def apply_section_filter(filter_name, filter_args, all_sections):
    """
    Returns sections after filtering based on ``filter_args``. It returns
    all sections if nothing is present in ``filter_args``.

    :param filter_name:
        Name of the filter.
    :param filter_args:
        Arguments of the filter to be passed in.
        For example:
        ``['tags', ('java',)]``
    :param all_bears:
        List of sections on which filter is to be applied.
        All the sections are loaded automatically by default.
    :return:
        Filtered sections based on a single filter.
    """
    if not is_valid_section_filter(filter_name):
        raise InvalidFilterException(filter_name)
    if not filter_args or len(filter_args) == 0:
        return all_bears

    # Args of section filters can be more than
    # strings, they can be objects.
    filter_function = available_section_filters[filter_name]

    filtered_sections = []
    for section in all_sections:
        if filter_function(section, filter_args):
            filtered_sections += [section]

    return filtered_sections


def apply_section_filters(filters, sections):
    """
    Returns sections after filtering based on ``filters``. It returns
    intersection of sections if more than one element is present in ``filters``
    list.

    :param filters:
        List of args based on ``sections`` has to be filtered.
        For example:
        ``[['tags', ('save', 'change')], ['exclude', ('css', '!python')]]``
    :param sections:
        The sections to filter.
    :return:
        Filtered sections.
    """
    for filter in filters:
        filter_name, *filter_args = filter
        sections = apply_section_filter(filter_name, filter_args, sections)

    return sections
