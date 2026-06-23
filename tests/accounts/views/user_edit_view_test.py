from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase


UserModel = get_user_model()


class UserEditViewTests(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    def test_edit_profile__always_edits_the_logged_in_user(self):
        # ProfileEdit.get_object() returns request.user, so the pk in the URL is
        # ignored and a user can only ever edit their own profile.
        profile_user = self._create_user_and_login({
            'username': self.VALID_TEACHER_DATA['username'] + '1',
            'password': self.VALID_TEACHER_DATA['password'],
            'email': '1' + self.VALID_TEACHER_DATA['email'],
            'user_type': 'student',
        })

        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('edit-user', kwargs={'pk': profile_user.pk}))

        self.assertEqual(200, response.status_code)
        self.assertEqual(user.pk, response.context['object'].pk)
