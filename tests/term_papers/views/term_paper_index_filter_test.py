from datetime import timedelta

from django.urls import reverse_lazy
from django.utils import timezone, translation

from final_project.term_papers.models import TermPaperRequest
from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import (
    create_active_term_paper,
    create_term_paper_request,
    create_user,
)


class TermPaperIndexFilterTests(BaseTestCase):
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

    def test_index__when_paper_is_active__expect_it_listed(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        create_active_term_paper(student)

        response = self.client.get(reverse_lazy('term-paper-index'))

        self.assertEqual(1, len(response.context['object_list']))

    def test_index__when_paper_is_taken__expect_excluded(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        teacher = create_user('teacher')
        create_active_term_paper(student, taken_by=teacher)

        response = self.client.get(reverse_lazy('term-paper-index'))

        self.assertEqual(0, len(response.context['object_list']))

    def test_index__when_paper_is_completed__expect_excluded(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        create_active_term_paper(student, completed=True)

        response = self.client.get(reverse_lazy('term-paper-index'))

        self.assertEqual(0, len(response.context['object_list']))

    def test_index__when_deadline_passed__expect_excluded(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        create_active_term_paper(
            student,
            death_line=timezone.now().date() - timedelta(days=1),
        )

        response = self.client.get(reverse_lazy('term-paper-index'))

        self.assertEqual(0, len(response.context['object_list']))

    def test_index__when_paper_has_pending_request__expect_excluded(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        teacher = create_user('teacher')
        paper = create_active_term_paper(student)
        create_term_paper_request(
            paper, student, teacher,
            status=TermPaperRequest.StatusChoices.PENDING,
        )

        response = self.client.get(reverse_lazy('term-paper-index'))

        self.assertEqual(0, len(response.context['object_list']))

    def test_index__search_by_title__expect_only_matching(self):
        student = self._create_user_and_login(self.VALID_STUDENT_DATA)
        create_active_term_paper(student, title='Machine Learning')
        create_active_term_paper(student, title='Ancient History')

        response = self.client.get(
            reverse_lazy('term-paper-index'), {'paper_title': 'Machine'}
        )

        titles = [p.title for p in response.context['object_list']]
        self.assertEqual(['Machine Learning'], titles)
