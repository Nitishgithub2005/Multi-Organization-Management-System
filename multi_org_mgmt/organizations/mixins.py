# organizations/mixins.py
from django.shortcuts import redirect
from django.contrib import messages

class OrganizationRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # Allow superusers to bypass organization check
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.organization:
            messages.error(request, 'You must be assigned to an organization to access this page.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class RoleRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # Allow superusers to bypass role check
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.role:
            messages.error(request, 'You must have a role assigned to access this page.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)