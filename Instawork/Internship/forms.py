from .models import Profile
from django import forms
from phonenumber_field.modelfields import PhoneNumberField

role_choices = (
    (False, "Regular can't delete"),
    (True, "Admin can delete"),
)

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Require first name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Require last name')
    email = forms.EmailField(max_length=254, required=True,help_text='Required. Inform a valid email address.')
    phone_number = PhoneNumberField(max_length=25, region='US')
    is_edit = forms.ChoiceField(label='Role', choices=role_choices, widget=forms.RadioSelect(), initial=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','email', 'phone_number', 'is_edit']