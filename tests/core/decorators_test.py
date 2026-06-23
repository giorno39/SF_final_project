from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.test import RequestFactory, TestCase

from final_project.core.decorators import allow_groups

UserModel = get_user_model()


def _protected_view(request):
    return 'VIEW_CALLED'


class AllowGroupsDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _request_with_user(self, user):
        request = self.factory.get('/')
        request.user = user
        return request

    def test_allow_groups__when_not_authenticated__expect_not_authenticated_response(self):
        view = allow_groups(['staff'])(_protected_view)
        request = self._request_with_user(AnonymousUser())

        response = view(request)

        self.assertEqual(b'Not authenticated!', response.content)

    def test_allow_groups__when_superuser__expect_view_called(self):
        superuser = UserModel.objects.create_superuser(
            username='admin', password='test_pass', email='admin@abv.bg',
        )
        view = allow_groups(['staff'])(_protected_view)
        request = self._request_with_user(superuser)

        self.assertEqual('VIEW_CALLED', view(request))

    def test_allow_groups__when_no_groups_required__expect_view_called(self):
        user = UserModel.objects.create_user(
            username='plain', password='test_pass', email='plain@abv.bg',
            user_type='student',
        )
        view = allow_groups()(_protected_view)
        request = self._request_with_user(user)

        self.assertEqual('VIEW_CALLED', view(request))

    def test_allow_groups__when_user_in_allowed_group__expect_view_called(self):
        user = UserModel.objects.create_user(
            username='member', password='test_pass', email='member@abv.bg',
            user_type='student',
        )
        group = Group.objects.create(name='reviewers')
        user.groups.add(group)

        view = allow_groups(['reviewers'])(_protected_view)
        request = self._request_with_user(user)

        self.assertEqual('VIEW_CALLED', view(request))

    def test_allow_groups__when_user_not_in_allowed_group__expect_forbidden_response(self):
        user = UserModel.objects.create_user(
            username='outsider', password='test_pass', email='outsider@abv.bg',
            user_type='student',
        )
        Group.objects.create(name='reviewers')

        view = allow_groups(['reviewers'])(_protected_view)
        request = self._request_with_user(user)

        response = view(request)

        self.assertEqual(b'Not in any of the allowed groups', response.content)
