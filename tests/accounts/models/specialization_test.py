from django.test import TestCase

from final_project.accounts.models import Specialization


class SpecializationModelTests(TestCase):
    def test_str__expect_name(self):
        # A migration seeds the standard specializations, so reuse safely.
        specialization, _ = Specialization.objects.get_or_create(name='Mathematics')

        self.assertEqual('Mathematics', str(specialization))

    def test_translated_name__when_known_name__expect_translation_entry(self):
        specialization, _ = Specialization.objects.get_or_create(name='Mathematics')

        self.assertEqual('Mathematics', str(specialization.translated_name))

    def test_translated_name__when_unknown_name__expect_same_name_back(self):
        specialization, _ = Specialization.objects.get_or_create(
            name='Underwater Basket Weaving'
        )

        self.assertEqual('Underwater Basket Weaving', specialization.translated_name)

    def test_ordering__expect_alphabetical_by_name(self):
        names = list(Specialization.objects.values_list('name', flat=True))

        # Meta.ordering = ('name',) so results always come back sorted.
        self.assertEqual(sorted(names), names)
