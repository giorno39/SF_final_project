from django.contrib.auth import get_user_model
from django.test import TestCase

from final_project.accounts.models import StudentProfile, TeacherProfile

UserModel = get_user_model()


class AppUserModelTests(TestCase):
    def test_str__expect_user_type_and_username(self):
        user = UserModel.objects.create_user(
            username='john', password='test_pass', email='john@abv.bg',
            user_type='teacher',
        )

        self.assertEqual('teacher;john', str(user))


class RoleProfileSignalTests(TestCase):
    def test_signal__when_teacher_created__expect_teacher_profile(self):
        user = UserModel.objects.create_user(
            username='teach', password='test_pass', email='teach@abv.bg',
            user_type='teacher',
        )

        self.assertTrue(TeacherProfile.objects.filter(user=user).exists())
        self.assertFalse(StudentProfile.objects.filter(user=user).exists())

    def test_signal__when_student_created__expect_student_profile(self):
        user = UserModel.objects.create_user(
            username='stud', password='test_pass', email='stud@abv.bg',
            user_type='student',
        )

        self.assertTrue(StudentProfile.objects.filter(user=user).exists())
        self.assertFalse(TeacherProfile.objects.filter(user=user).exists())

    def test_signal__when_reviewer_created__expect_no_role_profile(self):
        user = UserModel.objects.create_user(
            username='rev', password='test_pass', email='rev@abv.bg',
            user_type='reviewer',
        )

        self.assertFalse(TeacherProfile.objects.filter(user=user).exists())
        self.assertFalse(StudentProfile.objects.filter(user=user).exists())
