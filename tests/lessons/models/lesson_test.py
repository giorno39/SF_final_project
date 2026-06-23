from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from final_project.lessons.models import Lesson

UserModel = get_user_model()


class LessonModelTests(TestCase):
    def setUp(self):
        self.teacher = UserModel.objects.create_user(
            username='teacher', password='test_pass', email='teacher@abv.bg',
            user_type='teacher',
        )

    def test_valid_lesson__expect_no_error(self):
        lesson = Lesson(title='Algebra', price=30, teacher=self.teacher)

        # Should not raise.
        lesson.full_clean(exclude=('specializations',))

    def test_title_too_short__expect_validation_error(self):
        lesson = Lesson(title='A', price=30, teacher=self.teacher)

        with self.assertRaises(ValidationError):
            lesson.full_clean(exclude=('specializations',))

    def test_title_at_min_length__expect_no_error(self):
        lesson = Lesson(title='AB', price=30, teacher=self.teacher)

        # Two characters is exactly TITLE_MIN_LEN.
        lesson.full_clean(exclude=('specializations',))
