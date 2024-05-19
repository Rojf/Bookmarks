from core.repositories.Repository import UserRepository


class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return
        try:
            user = UserRepository.get(email=username)

            if user.check_password(password):
                return user
            return None
        except (UserRepository.model.DoesNotExist, UserRepository.model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return UserRepository.get(pk=user_id)
        except UserRepository.model.DoesNotExist:
            return None
