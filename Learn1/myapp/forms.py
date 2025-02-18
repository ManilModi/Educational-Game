from django import forms
from .models import Users

class LoginForm(forms.Form):
    
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('entrepreneur', 'Entrepreneur'),
        ('researcher', 'Researcher'),
        ('admin', 'Admin')
    ]
    user_type = forms.ChoiceField(label='User Type', choices=USER_TYPE_CHOICES)
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    
class UserRegistrationForm(forms.Form):
    
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('entrepreneur', 'Entrepreneur'),
        ('researcher', 'Researcher'),
        ('govt. engineer', 'Government Engineer'),
        ('admin', 'Admin')
    ]

    user_type = forms.ChoiceField(
        label='Register as',
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect
    )
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    company_name = forms.CharField(label='Company Name', max_length=255, required=False)
    institution = forms.CharField(label='Institution', max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'entrepreneur' and not cleaned_data.get('company_name'):
            self.add_error('company_name', 'Company name is required for Entrepreneurs.')

        if user_type == 'researcher' and not cleaned_data.get('institution'):
            self.add_error('institution', 'Institution is required for Researchers.')

        return cleaned_data

# class NormalUserForm(forms.Form):
#     USER_TYPE_CHOICES = [
#         ('Journlaist', 'Journalist'),
#         ('Student', 'Student'),
#     ]

#     username = forms.CharField(label='Username', max_length=50)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     user_type = forms.ChoiceField(label='User Type', choices=USER_TYPE_CHOICES)

# class EntrepreneurForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=50)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     company_name = forms.CharField(label='Company Name', max_length=255, required=False)


# class GovernmentEngineerForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=50)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     department = forms.CharField(label='Department', max_length=255, required=False)


# class ResearcherForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=50)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     institution = forms.CharField(label='Institution', max_length=255, required=False)


# class AdminForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=50)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)


