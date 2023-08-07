from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_trophies_for_teacher

UserModel = get_user_model()


class UserDetailsViewTests(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    def test_user_details__when_owner__expect_is_owner_true(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)
        response = self.client.get(reverse_lazy('details-user', kwargs={'pk': user.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_user_details__when_not_owner__expect_is_owner_false(self):
        profile_user = self._create_user_and_login({
            'username': self.VALID_TEACHER_DATA['username'] + '1',
            'password': self.VALID_TEACHER_DATA['password'],
            'email': '1' + self.VALID_TEACHER_DATA['email'],
            'user_type': 'student',
        })

        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('details-user', kwargs={'pk': profile_user.pk}))

        self.assertFalse(response.context['is_owner'])

    def test_user_details__when_teacher_with_trophies_expect_correct_avg_rate(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        create_trophies_for_teacher(user, count=2)

        response = self.client.get(reverse_lazy('details-user', kwargs={'pk': user.pk}))

        self.assertIsNotNone(response.context['avg_rate'])
        self.assertEquals(2.5, response.context['avg_rate'])

    def test_user_details__when_teacher_without_trophies_expect_no_avg_rate(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('details-user', kwargs={'pk': user.pk}))

        self.assertIsNone(response.context['avg_rate'])


