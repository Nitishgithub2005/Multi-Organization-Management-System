from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Organization, CustomUser, Role
from .forms import OrganizationForm, CustomUserCreationForm, RoleAssignmentForm
from .mixins import OrganizationRequiredMixin, RoleRequiredMixin

class OrganizationListView(LoginRequiredMixin, OrganizationRequiredMixin, RoleRequiredMixin, ListView):
    model = Organization
    template_name = 'organizations/organization_list.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.all()
        if user.is_main_org_admin():
            return Organization.objects.all()
        return Organization.objects.filter(id=user.organization.id)

class OrganizationEditView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, UpdateView):
    model = Organization
    fields = ['name', 'address', 'is_main']
    template_name = 'organizations/organization_form.html'
    success_url = reverse_lazy('organization-list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_organization_admin()

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to edit organizations.')
        return redirect('organization-list')

class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, DeleteView):
    model = Organization
    template_name = 'organizations/organization_confirm_delete.html'
    success_url = reverse_lazy('organization-list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_organization_admin()

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to delete organizations.')
        return redirect('organization-list')

class OrganizationCreateView(LoginRequiredMixin, UserPassesTestMixin, RoleRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organizations/organization_form.html'
    success_url = reverse_lazy('organization-list')

    def test_func(self):
        return self.request.user.is_main_org_admin()

    def handle_no_permission(self):
        messages.error(self.request, 'Only main organization admins can create new organizations.')
        return redirect('organization-list')

class UserListView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, ListView):
    model = CustomUser
    template_name = 'organizations/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        elif user.is_organization_admin():
            return CustomUser.objects.filter(organization=user.organization)
        elif user.is_editor():
            return CustomUser.objects.filter(organization=user.organization)
        elif user.is_viewer():
            return CustomUser.objects.filter(organization=user.organization)
        return CustomUser.objects.none()

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_organization_admin() or user.is_editor() or user.is_viewer()

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'organizations/user_form.html'

    def get_success_url(self):
        return reverse_lazy('organization-users', kwargs={'organization_id': self.request.user.organization.id})

    def test_func(self):
        user = self.request.user
        # Allow superuser, org admin, and editor to create users
        return user.is_superuser or user.is_organization_admin() or user.is_editor()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Superuser might not have an associated organization
        if self.request.user.is_superuser:
            kwargs['organization'] = None
        else:
            kwargs['organization'] = self.request.user.organization
        return kwargs

    def form_valid(self, form):
        # Assign organization only if user is not superuser
        if not self.request.user.is_superuser:
            form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class RoleAssignmentView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, UpdateView):
    model = CustomUser
    form_class = RoleAssignmentForm
    template_name = 'organizations/role_assignment.html'

    def get_success_url(self):
        return reverse_lazy('organization-users', kwargs={'organization_id': self.request.user.organization.id})

    def test_func(self):
        current_user = self.request.user
        target_user = self.get_object()

        if current_user.is_superuser:
            return True  # Super admin can assign roles to any user

        if current_user.is_editor() and target_user.is_organization_admin():
            return False

        if current_user.is_editor():
            return target_user.organization == current_user.organization

        if current_user.is_organization_admin():
            return target_user.organization == current_user.organization

        return False

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to assign or change this user\'s role.')
        return redirect('organization-users', organization_id=self.request.user.organization.id)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'organizations/user_form.html'

    def get_success_url(self):
        return reverse_lazy('organization-users', kwargs={'organization_id': self.object.organization.id})

    def test_func(self):
        if self.request.user.is_superuser:
            return True  # Super admin can update any user
        return (
            self.request.user.is_organization_admin() and
            self.get_object().organization == self.request.user.organization
        )

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, OrganizationRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'organizations/user_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('organization-users', kwargs={'organization_id': self.object.organization.id})

    def test_func(self):
        if self.request.user.is_superuser:
            return True  # Super admin can delete any user
        return (
            self.request.user.is_organization_admin() and
            self.get_object().organization == self.request.user.organization
        )

class OrganizationUsersView(LoginRequiredMixin, OrganizationRequiredMixin, ListView):
    model = CustomUser
    template_name = 'organizations/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        user = self.request.user

        if user.is_superuser or user.is_main_org_admin():
            return CustomUser.objects.filter(organization_id=organization_id)

        elif (user.organization and
              user.organization.id == organization_id and
              (user.is_organization_admin() or user.is_editor() or user.is_viewer())):
            return CustomUser.objects.filter(organization_id=organization_id)

        return CustomUser.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_id = self.kwargs['organization_id']
        context['organization'] = get_object_or_404(Organization, id=organization_id)
        return context
