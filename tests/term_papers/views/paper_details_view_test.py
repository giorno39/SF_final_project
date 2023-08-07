from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user


class PaperDetailsViewTest(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    VALID_STUDENT_DATA = {
        'username': VALID_TEACHER_DATA['username'] + '1',
        'password': VALID_TEACHER_DATA['password'],
        'email': '1' + VALID_TEACHER_DATA['email'],
        'user_type': 'student',
    }

    def test_paper_details__when_accessed_by_owner_and_is_taken__expect_both_to_be_true(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)


        paper = create_term_paper_for_1_user(profile_user)
        paper.taken_by = user
        paper.save()

        response = self.client.get(reverse_lazy('term-paper-details', kwargs={'pk': paper.pk}))

        self.assertTrue(response.context['is_owner'])
        self.assertIsNotNone(response.context['is_taken'])


    def test_paper_details__when_not_accessed_by_the_owner_and_is_not_taken_expect_both_to_be_false(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(profile_user)

        response = self.client.get(reverse_lazy('term-paper-details', kwargs={'pk': paper.pk}))

        self.assertFalse(response.context['is_owner'])
        self.assertIsNone(response.context['is_taken'])

