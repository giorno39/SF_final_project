from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_active_term_paper, create_user


class CreateTrophyViewTest(BaseTestCase):
    VALID_STUDENT_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'student',
    }

    def test_create_trophy_view__attach_the_trophy_to_the_correct_project__expect_right_paper_pk(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        teacher = create_user('teacher')
        paper = create_active_term_paper(student, taken_by=teacher)

        response = self.client.get(reverse_lazy('trophy-add', kwargs={'paper_pk': paper.pk}))

        self.assertEqual(paper.pk, response.context['pk_paper'])

    def test_create_trophy__set_term_paper_to_be_rated__expect_rated_to_become_true(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        teacher = create_user('teacher')
        paper = create_active_term_paper(student, taken_by=teacher)

        response = self.client.post(
            reverse_lazy('trophy-add', kwargs={'paper_pk': paper.pk}),
            data={'rate': 5, 'comment': 'Great work'},
        )
        paper.refresh_from_db()

        self.assertTrue(paper.rated)
