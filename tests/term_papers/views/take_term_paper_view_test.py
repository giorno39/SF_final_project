from django.urls import reverse_lazy

from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_paper_for_1_user


class TakeTermPaperViewTest(BaseTestCase):
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

    def test_take_term_paper__when_tried_to_be_accessed_by_a_student__expect_to_be_redirected_and_not_taken(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)

        paper = create_term_paper_for_1_user(profile_user)

        response = self.client.get(reverse_lazy('term-paper-take', kwargs={'pk': paper.pk}))

        expected_url = reverse_lazy('term-paper-details', kwargs={'pk': paper.pk})
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

        self.assertIsNone(paper.taken_by)

    def test_take_term_paper__when_accessed_by_a_teacher_expect_to_be_redirected_and_taken(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        paper = create_term_paper_for_1_user(profile_user)

        response = self.client.get(reverse_lazy('term-paper-take', kwargs={'pk': paper.pk}))

        paper.refresh_from_db()

        self.assertEqual(paper.taken_by_id, user.pk)

        expected_url = reverse_lazy('term-paper-details', kwargs={'pk': paper.pk})
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

