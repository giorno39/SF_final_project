from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from final_project.useful_materials.models import MaterialComment, MaterialCommentVote
from tests.utils.creation_utils import (
    create_material_comment,
    create_material_for_1_user,
    create_user,
)

UserModel = get_user_model()


class MaterialCommentTests(TestCase):
    def setUp(self):
        self.author = create_user('teacher')
        self.material = create_material_for_1_user(self.author)

    def test_str__expect_author_and_material(self):
        comment = create_material_comment(self.material, self.author, content='great')

        self.assertEqual(
            f'Comment by {self.author} on {self.material}',
            str(comment),
        )

    def test_ordering__expect_newest_first(self):
        first = create_material_comment(self.material, self.author, content='first')
        second = create_material_comment(self.material, self.author, content='second')

        # created_at uses auto_now_add, so on coarse-resolution clocks both rows
        # can share a timestamp. Set explicit, distinct times to test ordering.
        now = timezone.now()
        MaterialComment.objects.filter(pk=first.pk).update(
            created_at=now - timedelta(minutes=5)
        )
        MaterialComment.objects.filter(pk=second.pk).update(created_at=now)

        comments = list(self.material.comments.all())

        # Meta ordering is '-created_at' so the most recent comment comes first.
        self.assertEqual([second.pk, first.pk], [c.pk for c in comments])


class MaterialCommentVoteTests(TestCase):
    def setUp(self):
        self.author = create_user('teacher')
        self.voter = create_user('student')
        self.material = create_material_for_1_user(self.author)
        self.comment = create_material_comment(self.material, self.author)

    def test_vote__when_user_votes_twice__expect_integrity_error(self):
        MaterialCommentVote.objects.create(comment=self.comment, user=self.voter)

        with self.assertRaises(IntegrityError):
            MaterialCommentVote.objects.create(comment=self.comment, user=self.voter)
