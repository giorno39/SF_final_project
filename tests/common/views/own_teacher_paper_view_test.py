from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from final_project.term_papers.models import TermPaper
from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_papers_for_2_users, create_completed_term_paper

UserModel = get_user_model()


class OwnTeacherPaperViewTests(BaseTestCase):
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

    def test_teacher_paper__when_student_tries_to_access_them__expect_redirect_to_teacher_papers(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)



        response = self.client.get(reverse_lazy('student-papers'))

        expected_url = reverse_lazy('teacher-papers')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

#TODO CHECK THIS TEST
    def test_teacher_paper__when_has_to_show_only_taken_expect_correct_number_of_papers(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        create_term_papers_for_2_users(user, profile_user, count=3)

        response = self.client.get(reverse_lazy('teacher-papers'))
        papers = response.context['object_list']
        self.assertEqual(3, len(papers))


    def test_teacher_paper__when_there_are_only_completed_papers_expect_no_papers(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        create_completed_term_paper(user)

        response = self.client.get(reverse_lazy('teacher-papers'))
        papers = response.context['object_list']
        self.assertEqual(0, len(papers))
