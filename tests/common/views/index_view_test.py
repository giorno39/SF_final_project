from django.urls import reverse_lazy
from django.utils import translation

from tests.accounts.base_test_case import BaseTestCase


class IndexViewTest(BaseTestCase):
    VALID_STUDENT_DATA = {
        'username': 'student',
        'password': 'test_pass',
        'email': 'student@abv.bg',
        'user_type': 'student',
    }

    def setUp(self):
        # URLs are served under i18n language prefixes; pin a supported
        # language so reverse() produces a resolvable path.
        translation.activate('en')
        self.addCleanup(translation.deactivate)

    def test_index__when_anonymous__expect_base_template(self):
        response = self.client.get(reverse_lazy('index'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'base/base.html')

    def test_index__when_authenticated__expect_accounts_template(self):
        self._create_user_and_login(self.VALID_STUDENT_DATA)

        response = self.client.get(reverse_lazy('index'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'common/index-accounts.html')
