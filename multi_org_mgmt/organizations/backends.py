from django.contrib.auth.backends import ModelBackend

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        is_active = super().user_can_authenticate(user)
        if not is_active or user is None:
            return False
            
        # Allow superusers to bypass organization and role checks
        if user.is_superuser:
            return True
            
        # For regular users, check organization and role
        return user.organization is not None and user.role is not None