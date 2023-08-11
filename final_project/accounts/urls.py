from django.urls import path

from final_project.accounts.views import SignInView, SignUpView, SignOutView, ProfileDetails, ProfileEdit, \
    ProfileDelete, ChangePasswordView

urlpatterns = (
    path('login/', SignInView.as_view(), name='login-user'),
    path('register/', SignUpView.as_view(), name='register-user'),
    path('logout/', SignOutView.as_view(), name='logout-user'),
    path('details-profile/<int:pk>/', ProfileDetails.as_view(), name='details-user'),
    path('edit-profile/<int:pk>', ProfileEdit.as_view(), name='edit-user'),
    path('delete-profile/<int:pk>', ProfileDelete.as_view(), name='delete-user'),
    path('chage-pass/', ChangePasswordView.as_view(), name='change-password')
)
