from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from final_project.trophies.models import Trophy

UserModel = get_user_model()


class TrophyModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='teacher', password='test_pass', email='teacher@abv.bg',
            user_type='teacher',
        )

    def test_default_rate_is_zero(self):
        trophy = Trophy.objects.create(completed_by=self.user)

        self.assertEqual(0, trophy.rate)

    def test_rate_within_bounds__expect_valid(self):
        trophy = Trophy(rate=3, project='DB', completed_by=self.user)

        # Should not raise.
        trophy.full_clean()

    def test_rate_above_max__expect_validation_error(self):
        trophy = Trophy(rate=6, project='DB', completed_by=self.user)

        with self.assertRaises(ValidationError):
            trophy.full_clean()

    def test_rate_below_min__expect_validation_error(self):
        trophy = Trophy(rate=-1, project='DB', completed_by=self.user)

        with self.assertRaises(ValidationError):
            trophy.full_clean()

    def test_comment_too_long__expect_validation_error(self):
        trophy = Trophy(rate=3, completed_by=self.user, comment='x' * 156)

        with self.assertRaises(ValidationError):
            trophy.full_clean()
