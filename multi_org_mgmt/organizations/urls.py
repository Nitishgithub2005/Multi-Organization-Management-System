from django.urls import path
from . import views

urlpatterns = [
    # Organization URLs
    path('', views.OrganizationListView.as_view(), name='organization-list'),
    path('organization/create/', views.OrganizationCreateView.as_view(), name='organization-create'),
    path('organization/<int:pk>/edit/', views.OrganizationEditView.as_view(), name='organization-edit'),
    path('organization/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization-delete'),
    path('organization/<int:organization_id>/users/', views.OrganizationUsersView.as_view(), name='organization-users'),
    
    # User URLs
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-update'),  # Added missing user update URL
    path('users/<int:pk>/role/', views.RoleAssignmentView.as_view(), name='role-assignment'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]