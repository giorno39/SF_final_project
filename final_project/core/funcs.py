from django.contrib.auth import get_user_model

UserModel = get_user_model()


def get_user_by_id(pk):
    return UserModel.objects. \
        filter(pk=pk). \
        get()
