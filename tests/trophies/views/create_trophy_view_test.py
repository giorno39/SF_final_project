from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user


class CreateTrophyViewTest(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    def test_create_trophy_view__attach_the_trophy_to_the_correct_project__expect_right_paper_pk(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(user)

        response = self.client.get(reverse_lazy('trophy-add', kwargs={'paper_pk': paper.pk}))

        self.assertEqual(paper.pk, response.context['pk_paper'])


    def test_create_trophy__set_term_paper_to_be_rated__expect_rated_to_become_true(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(user, taken=user)

        response = self.client.post(reverse_lazy('trophy-add', kwargs={'paper_pk': paper.pk}))
        paper.refresh_from_db()

        self.assertEqual(True, paper.rated)