from django.contrib.auth import get_user_model
from django.test import TestCase

from final_project.accounts.models import TeacherProfile

UserModel = get_user_model()


class TeacherProfileTrustTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='teacher', password='test_pass', email='teacher@abv.bg',
            user_type='teacher',
        )
        # Auto-created by the post_save signal.
        self.profile = TeacherProfile.objects.get(user=self.user)

    def test_default_trust_score(self):
        self.assertEqual(50, self.profile.trust_score)

    def test_increase_trust__within_bounds(self):
        self.profile.increase_trust(10)

        self.assertEqual(60, self.profile.trust_score)

    def test_increase_trust__cannot_exceed_max(self):
        self.profile.increase_trust(1000)

        self.assertEqual(TeacherProfile.MAX_TRUST_SCORE, self.profile.trust_score)

    def test_decrease_trust__within_bounds(self):
        self.profile.decrease_trust(20)

        self.assertEqual(30, self.profile.trust_score)

    def test_decrease_trust__cannot_go_below_min(self):
        self.profile.decrease_trust(1000)

        self.assertEqual(TeacherProfile.MIN_TRUST_SCORE, self.profile.trust_score)

    def test_str__expect_username_wrapped(self):
        self.assertEqual('TeacherProfile<teacher>', str(self.profile))
