from django.urls import reverse_lazy

from final_project.lessons.models import Lesson
from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_lesson_for_1_user


class LessonDetailsViewTest(BaseTestCase):
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

    def test_lesson_details__when_accessed_by_the_creator_expect_is_owner_true(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        lesson = create_lesson_for_1_user(user)

        response = self.client.get(reverse_lazy('lesson-details', kwargs={'pk': lesson.pk}))

        self.assertTrue(response.context['is_owner'])


    def test_lesson_details__when_accessed_not_by_owner_expect_is_owner_false(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)

        lesson = create_lesson_for_1_user(user)

        response = self.client.get(reverse_lazy('lesson-details', kwargs={'pk': lesson.pk}))

        self.assertFalse(response.context['is_owner'])

