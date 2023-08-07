from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user


class PaperIndexViewTest(BaseTestCase):
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

    def test_index_paper_view__when_there_are_only_old_papers__expect_empty_queryset(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(user)

        response = self.client.get(reverse_lazy('term-paper-index'))
        queryset = response.context['object_list']
        self.assertEqual(0, len(queryset))


    def test_index_paper_view__when_there_is_a_active_paper__expect_correct_queryset(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(user, date='2024-07-19')

        response = self.client.get(reverse_lazy('term-paper-index'))
        queryset = response.context['object_list']
        self.assertEqual(1, len(queryset))
