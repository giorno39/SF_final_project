from django.contrib.auth import get_user_model
from django.test import TestCase

from final_project.core.funcs import get_user_by_id

UserModel = get_user_model()


class GetUserByIdTests(TestCase):
    def test_get_user_by_id__when_user_exists__expect_correct_user(self):
        user = UserModel.objects.create_user(
            username='someone',
            password='test_pass',
            email='someone@abv.bg',
            user_type='student',
        )

        result = get_user_by_id(user.pk)

        self.assertEqual(user.pk, result.pk)
        self.assertEqual('someone', result.username)

    def test_get_user_by_id__when_user_does_not_exist__expect_does_not_exist(self):
        with self.assertRaises(UserModel.DoesNotExist):
            get_user_by_id(999999)
