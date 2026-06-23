from django.urls import reverse_lazy

from final_project.lessons.models import Lesson
from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_lessons_from_2_users


class OwnLessonViewTest(BaseTestCase):
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

    def test_own_lesson_view__when_accessed_by_owner_expect_correct_number_of_lessons(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        create_lessons_from_2_users(user, profile_user)

        response = self.client.get(reverse_lazy('own-lesson-index'))
        queryset = response.context['object_list']
        self.assertEqual(2, len(queryset))

    def test_own_lesson_view__when_accessed_by_a_student_expect_no_perms(self):
        self._create_user_and_login(self.VALID_STUDENT_DATA)

        response = self.client.get(reverse_lazy('own-lesson-index'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'common/no-perms.html')
