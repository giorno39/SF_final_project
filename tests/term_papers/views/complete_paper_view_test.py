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

    def test_complete_paper__when_accessed_not_by_the_user_that_took_the_paper__expect_not_found(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        # Paper taken by the student, not by the logged-in teacher.
        paper = create_term_paper_for_1_user(profile_user, taken=profile_user)

        response = self.client.get(reverse_lazy('term-paper-complete', kwargs={'pk': paper.pk}))

        # The view's queryset only contains papers taken by request.user, so this
        # paper is invisible to the teacher and the lookup 404s.
        self.assertEqual(404, response.status_code)
