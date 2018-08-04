import unittest

from coalib.parsing.FilterHelper import (
    apply_filter,
    apply_filters,
    apply_section_filter,
    apply_section_filters,
    is_valid_filter,
    is_valid_section_filter,
    collect_cli_section_filters,
    _filter_section_bears
)
from coalib.parsing.filters import available_filters
from coalib.parsing.InvalidFilterException import InvalidFilterException
from coalib.settings.ConfigurationGathering import get_all_bears
from coalib.settings.Section import Section, Setting
from coalib.parsing.DefaultArgParser import default_arg_parser


class MockParsedArgs:

    def __init__(self, **kargs):
        for k, v in kargs.items():
            setattr(self, k, v)


class FilterHelperTest(unittest.TestCase):

    def sample_sections(self, count):
        sections = []
        for l in range(count):
            sections += [Section('sec'+str(l))]

        return sections

    def test_apply_filter_exception(self):
        with self.assertRaises(InvalidFilterException) as exp:
            apply_filter('unknown', ['args'])

        message = str(exp.exception)
        self.assertEqual("'unknown' is an invalid filter. Available filters: "
                         + ', '.join(sorted(available_filters)), message)

    def test_apply_section_filter_exception(self):
        with self.assertRaises(InvalidFilterException) as exp:
            apply_section_filter('unknown', ['args'], [])

    def test_is_valid_filter_true(self):
        filter_result = is_valid_filter('can_detect')
        self.assertTrue(filter_result)

    def test_is_valid_filter_false(self):
        filter_result = is_valid_filter('wrong_filter')
        self.assertFalse(filter_result)

    def test_is_valid_section_filter_false(self):
        filter_result = is_valid_section_filter('bad_section_filter')
        self.assertFalse(filter_result)

    def test_is_valid_section_filter_true(self):
        filter_result = is_valid_section_filter('tag_section_filter')
        self.assertTrue(filter_result)

    def test_filter_section_bears(self):
        local_bears = get_all_bears()[0]
        filter_args = {'c', 'java'}
        result_for_filter_section = _filter_section_bears(
            local_bears, filter_args, 'language')
        self.assertIsNotNone(result_for_filter_section)

    def test_apply_filter(self):
        apply_filter_result = apply_filter('language', ['c', 'java'])
        self.assertIsNotNone(apply_filter_result)

    def test_apply_filters(self):
        apply_filters_result = apply_filters([('language', 'C', 'Python'),
                                              ('can_fix', 'syntax')])
        self.assertIsNotNone(apply_filters_result)

    def test_apply_section_filter_empty(self):
        filtered = apply_section_filter('tag_section_filter', ['args'], [])
        self.assertEqual(filtered, [])

        # Empty args
        filtered = apply_section_filter('tag_section_filter', [], [])
        self.assertEqual(filtered, [])

    def test_apply_section_filter(self):
        secs = self.sample_sections(4)

        secs[0].append(Setting('tags', 'save'))
        secs[1].append(Setting('tags', 'change'))

        filtered = apply_section_filter('tag_section_filter',
                                        [['save', 'change']], secs)
        self.assertEqual(len(filtered), 2)

    def test_apply_section_filters_empty(self):
        secs = self.sample_sections(4)

        filtered = apply_section_filters([], secs)
        self.assertEqual(len(filtered), 4)

    def test_apply_section_filters(self):
        secs = self.sample_sections(4)

        secs[0].append(Setting('tags', 'save'))
        secs[1].append(Setting('tags', 'change'))
        secs[3].append(Setting('tags', 'some_other_tag'))

        filters = [['tag_section_filter', ['save', 'change']]]
        filtered = apply_section_filters(filters, secs)

        self.assertEqual(len(filtered), 2)

    def test_collect_cli_section_filters_empty(self):
        filters = collect_cli_section_filters(MockParsedArgs())
        self.assertEqual(len(filters), 0)

    def test_collect_cli_section_filters(self):
        args = MockParsedArgs(tags=['save'])
        filters = collect_cli_section_filters(args)
        self.assertEqual(filters[0], ['tag_section_filter', ['save']])

    def test_collect_cli_section_filters_from_list(self):
        filters = collect_cli_section_filters(None, ['--tags', 'save'])
        self.assertEqual(filters[0], ['tag_section_filter', ['save']])

    def test_collect_cli_section_filters_with_parser(self):
        filters = collect_cli_section_filters(None,
                                              ['--tags', 'hello'],
                                              default_arg_parser())
        self.assertEqual(filters[0], ['tag_section_filter', ['hello']])
