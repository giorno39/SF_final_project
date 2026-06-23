from django.test import TestCase

from final_project.accounts.forms import UserCreateForm


class UserCreateFormTests(TestCase):
    def _valid_data(self, **overrides):
        data = {
            'username': 'newuser',
            'email': 'newuser@abv.bg',
            'user_type': 'student',
            'password1': 'sup3r-secret-pw',
            'password2': 'sup3r-secret-pw',
        }
        data.update(overrides)
        return data

    def test_user_type_choices__expect_only_student_and_teacher(self):
        form = UserCreateForm()
        values = [value for value, _ in form.fields['user_type'].choices]

        self.assertIn('student', values)
        self.assertIn('teacher', values)
        self.assertNotIn('reviewer', values)

    def test_valid_data__expect_form_valid(self):
        form = UserCreateForm(data=self._valid_data())

        self.assertTrue(form.is_valid())

    def test_password_mismatch__expect_form_invalid(self):
        form = UserCreateForm(
            data=self._valid_data(password2='different-pw')
        )

        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
