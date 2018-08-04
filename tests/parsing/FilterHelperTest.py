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


class MockParsedArgs:

    def __init__(self, **kargs):
        for k, v in kargs.items():
            setattr(self, k, v)


class FilterHelperTest(unittest.TestCase):

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
        filtered = apply_section_filter('section_filter', ['args'], [])
        self.assertEqual(filtered, [])

        # Empty args
        filtered = apply_section_filter('section_filter', [], [])
        self.assertEqual(filtered, [])

    def test_collect_cli_section_filters_empty(self):
        filters = collect_cli_section_filters(MockParsedArgs())
        self.assertEqual(len(filters), 0)
