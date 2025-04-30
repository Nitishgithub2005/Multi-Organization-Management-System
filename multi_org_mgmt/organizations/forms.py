from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Organization, CustomUser, Role

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add email field explicitly

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'organization', 'role')

    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        user = kwargs.pop('user', None)  # Get current user

        super().__init__(*args, **kwargs)

        if organization:
            self.fields['organization'].initial = organization
            self.fields['organization'].widget = forms.HiddenInput()

        # If the current user is an editor, restrict role choices
        if user and user.role.name == 'EDITOR':
            self.fields['role'].queryset = Role.objects.exclude(name='ADMIN')

class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']