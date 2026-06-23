from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase


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

    def test_create_view__when_accessed_by_a_teacher_expect_no_perms(self):
        self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('term-paper-add'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'common/no-perms.html')
