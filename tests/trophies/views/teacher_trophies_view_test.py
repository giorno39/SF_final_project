from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user, create_trophies_for_teacher


class TeacherTrophyViewTest(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    def test_teacher_trophies__when_called__expect_to_return_only_self_trophies(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        trophy = create_trophies_for_teacher(user)

        response = self.client.get(reverse_lazy('teacher-trophy', kwargs={'teacher': user.pk}))
        queryset = response.context['object_list']
        self.assertEqual(2, queryset.count())