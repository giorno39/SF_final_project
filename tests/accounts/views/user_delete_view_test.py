from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_trophies_for_teacher

UserModel = get_user_model()


class UserDeleteViewTests(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    def test_delete_profile__when_someone_else_tries_to_access_expect_redirect(self):
        profile_user = self._create_user_and_login({
            'username': self.VALID_TEACHER_DATA['username'] + '1',
            'password': self.VALID_TEACHER_DATA['password'],
            'email': '1' + self.VALID_TEACHER_DATA['email'],
            'user_type': 'student',
        })

        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('delete-user', kwargs={'pk': profile_user.pk}))

        expected_url = reverse_lazy('details-user', kwargs={'pk': profile_user.pk})
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
