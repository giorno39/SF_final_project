from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user


class PaperCreateViewTest(BaseTestCase):
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

    def test_create_view__when_accessed_by_a_teacher_expect_redirect(self):
        self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('term-paper-add'))

        expected_url = reverse_lazy('index')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)