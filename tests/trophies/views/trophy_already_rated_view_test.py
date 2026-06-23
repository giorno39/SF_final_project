from django.urls import reverse_lazy
from django.utils import translation

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_active_term_paper


class TrophyAlreadyRatedViewTest(BaseTestCase):
    VALID_STUDENT_DATA = {
        'username': 'student',
        'password': 'test_pass',
        'email': 'student@abv.bg',
        'user_type': 'student',
    }

    def setUp(self):
        translation.activate('en')
        self.addCleanup(translation.deactivate)

    def test_create_trophy__when_paper_already_rated__expect_already_rated_template(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        paper = create_active_term_paper(student, rated=True)

        response = self.client.get(
            reverse_lazy('trophy-add', kwargs={'paper_pk': paper.pk})
        )

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'trophies/trophy-already-rated.html')

    def test_create_trophy__when_paper_not_rated__expect_add_form(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        paper = create_active_term_paper(student, rated=False)

        response = self.client.get(
            reverse_lazy('trophy-add', kwargs={'paper_pk': paper.pk})
        )

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'trophies/trophy-add.html')
        self.assertEqual(paper.pk, response.context['pk_paper'])
