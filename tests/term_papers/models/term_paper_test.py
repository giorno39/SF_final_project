from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from final_project.term_papers.models import TermPaper
from tests.utils.creation_utils import create_active_term_paper, create_user

UserModel = get_user_model()


class TermPaperModelTests(TestCase):
    def setUp(self):
        self.student = create_user('student')

    def test_defaults__expect_not_completed_not_rated_not_taken(self):
        paper = create_active_term_paper(self.student)

        self.assertFalse(paper.completed)
        self.assertFalse(paper.rated)
        self.assertIsNone(paper.taken_by)

    def test_title_too_short__expect_validation_error(self):
        paper = TermPaper(
            title='a',
            university='uni',
            death_line='2030-01-01',
            price_cap=10,
            content='term_paper_files/dummy.pdf',
            user=self.student,
        )

        # Exclude the M2M and the file field (no real file on disk in tests).
        with self.assertRaises(ValidationError):
            paper.full_clean(exclude=('specializations', 'content'))
