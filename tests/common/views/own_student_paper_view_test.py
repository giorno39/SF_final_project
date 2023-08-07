from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from final_project.term_papers.models import TermPaper
from tests.accounts.base_test_case import BaseTestCase
from tests.utils.creation_utils import create_term_papers_for_2_users

UserModel = get_user_model()


class OwnStudentPaperViewTests(BaseTestCase):
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

    def test_student_paper__when_teacher_tries_to_access_them__expect_redirect_to_teacher_papers(self):
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)

        response = self.client.get(reverse_lazy('student-papers'))

        expected_url = reverse_lazy('teacher-papers')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)


    def test_student_paper__when_has_to_show_only_selfpapers_expect_correct_number_of_papers(self):
        user = self._create_user_and_login(self.VALID_TEACHER_DATA)
        profile_user = self._create_user_and_login(self.VALID_STUDENT_DATA)

        create_term_papers_for_2_users(user, profile_user)



        response = self.client.get(reverse_lazy('student-papers'))
        papers = response.context['object_list']
        self.assertEqual(2, len(papers))




