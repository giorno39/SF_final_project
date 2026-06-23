from enum import Enum

from django.test import SimpleTestCase

from final_project.core.model_mixins import NumberChoicesEnumMixin


class _SampleChoices(NumberChoicesEnumMixin, Enum):
    SHORT = 1
    A_LONGER_NAME = 22


class NumberChoicesEnumMixinTests(SimpleTestCase):
    def test_choices__expect_name_value_pairs(self):
        self.assertEqual(
            [('SHORT', 1), ('A_LONGER_NAME', 22)],
            _SampleChoices.choices(),
        )

    def test_max_type_length__expect_length_of_longest_name(self):
        self.assertEqual(len('A_LONGER_NAME'), _SampleChoices.max_type_length())
