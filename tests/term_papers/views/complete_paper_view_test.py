from django.urls import reverse_lazy

from final_project.completed_papers.models import CompletedPaper
from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user


class CompleteTermPaperViewTest(BaseTestCase):
    VALID_TEACHER_DATA = {
        'username': 'test_user',
        'password': 'test_pass',
        'email': 'test@abv.bg',
        'user_type': 'teacher',
    }

    VALID_STUDENT_DATA = {
        'username': VALID_TEACHER_DATA['username'] + '1',
        'password': VALID_TEACHER_DATA['password'],
        'email': '1' + VALID_TEACHER_DATA['email'],
        'user_type': 'student',
    }

    def test_complete_paper__when__accessed_not_by_the_user_that_took_the_paper__expect_redirect(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(profile_user, taken=profile_user)

        response = self.client.get(reverse_lazy('term-paper-complete', kwargs={'pk': paper.pk}))

        expected_url = reverse_lazy('term-paper-details', kwargs={
            'pk': paper.pk,
        })
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_complete_paper__when_trying_to_complete_a_paper__expect_a_completed_paper_to_be_created(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(profile_user, taken=user)

        response = self.client.post(reverse_lazy('term-paper-complete', kwargs={'pk': paper.pk}))

        paper.refresh_from_db()
        papers = CompletedPaper.objects.all()

        self.assertTrue(paper.completed)
        self.assertEqual(1, len(papers))
