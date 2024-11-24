Django Multi-Organization Management Project

Project Overview

This project is a Django-based web application designed to manage multiple organizations, their users, and user roles. The system provides role-based access control for managing users within organizations.

Features

 1. Multi-organization support with role-based access control.
 2. Custom user model with extended fields for organizations and roles.
 3. Admin interface with advanced filtering and role assignment.
 4. User-friendly templates for managing users and organizations.
 5. Import/export functionality for user data using django-import-export.

Project Structure
multi_org_mgmt/
├── manage.py
├── multi_org_mgmt/
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
├── organizations/
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── backends.py
│ ├── mixins.py
│ ├── tests.py
│ ├── urls.py
│ ├── views.py
│ ├── forms.py
└── templates/
    ├── organization/
        ├── organization_confirm_delete.html
        ├── organization_form.html
        ├── organization_list.html
        ├── role_assignment.html
        ├── user_confirm_delete.html
        ├── user_form.html
        ├── user_list.html
    ├── registration/
        ├── login.html

Customizations

 1. Custom User Model:
 • Extended to include organization and role fields.
 • Allows assigning users to specific organizations and roles.
 2. Admin Panel Enhancements:
 • Customized UserAdmin to display organization and role information.
 • Added filtering options for organization and role in the admin panel.
 3. Import/Export Functionality:
 • Integrated django-import-export to handle user data import/export.
 • Configured CustomUserResource in resources.py for managing user data.

Assumptions

 1. Each user belongs to a single organization and has one role.
 2. Only admins can add/edit users and assign roles.
 3. The django-import-export package is used for managing bulk user data.

Setting Up and Running the Project Locally
Prerequisites

 1. Python 3.8 or higher
 2. pip (Python package manager)
 3. Virtual environment tool (e.g., venv or virtualenv)

Setup Instructions
1. Clone the Repository:
git clone <repository_url>
cd multi_org_mgmt

 2. Create and Activate a Virtual Environment:
python3 -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

 3. Install Dependencies:
pip install -r requirements.txt

 4. Install django-import-export:
pip install django-import-export

 5. Add import_export to INSTALLED_APPS:
Update INSTALLED_APPS in multi_org_mgmt/settings.py:
INSTALLED_APPS = [
    # Other apps
    'import_export',
]

 6. Apply Migrations:
python3 manage.py makemigrations
python3 manage.py migrate

 7. Create a Superuser:
python3 manage.py createsuperuser


 8. Run the Development Server:
python3 manage.py runserver 

 Usage Instructions

Admin Credentials

 1. Superadmin:
 • Username: mainadmin
 • Email: main@gmail.com
 • Password: admin@123

Department Users

IT Department

 • Admin:
 • Username: person1
 • Password: nitish@123

 • Editor:
 • Username: editor1
 • Password: nitish@123

 • Viewer:
 • Username: viewer1
 • Password: nitish@123

Research Department

 • Admin:
 • Username: person2
 • Password: nitish@123

 • Editor:
 • Username: editor2
 • Password: nitish@123

 • Viewer:
 • Username: viewer2
 • Password: nitish@123


Additional Notes

 • Make sure to restart the server after installing new packages or making significant changes to the code.
 • Use the admin panel for managing users and organizations efficiently.
 • The import/export feature can be accessed through the admin panel for bulk operations on user data.
