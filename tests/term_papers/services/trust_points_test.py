from datetime import timedelta
from types import SimpleNamespace

from django.test import SimpleTestCase
from django.utils import timezone

from final_project.term_papers.views import (
    get_completion_reward_points,
    get_unassign_penalty_points,
    is_late_unassignment,
)


def _paper_due_in(days):
    """Lightweight stand-in for a TermPaper exposing only ``death_line``."""
    return SimpleNamespace(death_line=timezone.now().date() + timedelta(days=days))


class UnassignPenaltyPointsTests(SimpleTestCase):
    def test_overdue__expect_4_points(self):
        self.assertEqual(4, get_unassign_penalty_points(_paper_due_in(-1)))

    def test_within_a_week__expect_3_points(self):
        self.assertEqual(3, get_unassign_penalty_points(_paper_due_in(3)))

    def test_within_two_weeks__expect_2_points(self):
        self.assertEqual(2, get_unassign_penalty_points(_paper_due_in(10)))

    def test_far_in_the_future__expect_1_point(self):
        self.assertEqual(1, get_unassign_penalty_points(_paper_due_in(30)))


class IsLateUnassignmentTests(SimpleTestCase):
    def test_seven_days_or_fewer__expect_true(self):
        self.assertTrue(is_late_unassignment(_paper_due_in(7)))

    def test_more_than_a_week__expect_false(self):
        self.assertFalse(is_late_unassignment(_paper_due_in(8)))


class CompletionRewardPointsTests(SimpleTestCase):
    def test_two_weeks_early__expect_3_points(self):
        self.assertEqual(3, get_completion_reward_points(_paper_due_in(20)))

    def test_one_week_early__expect_2_points(self):
        self.assertEqual(2, get_completion_reward_points(_paper_due_in(8)))

    def test_on_time__expect_1_point(self):
        self.assertEqual(1, get_completion_reward_points(_paper_due_in(2)))

    def test_overdue__expect_0_points(self):
        self.assertEqual(0, get_completion_reward_points(_paper_due_in(-1)))
