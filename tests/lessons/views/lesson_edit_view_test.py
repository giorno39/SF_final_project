from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_lesson_for_1_user


class LessonEditViewTest(BaseTestCase):
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

    def test_lesson_edit__when_not_accessed_by_the_creator__expect_redirect(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)

        lesson = create_lesson_for_1_user(user)

        response = self.client.get(reverse_lazy('lesson-edit', kwargs={'pk': lesson.pk}))

        expected_url = reverse_lazy('lesson-details', kwargs={'pk': lesson.pk})
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)






