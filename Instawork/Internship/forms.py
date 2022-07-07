from tkinter.font import families
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
role_choices = (
    (False, "Regular can't delete"),
    (True, "Admin can delete"),
)
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Require first name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Require last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')   
    is_edit = forms.ChoiceField(label='Role',choices=role_choices, widget=forms.RadioSelect(),initial=False)
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','phone_number','is_edit')
   

class AddForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Require first name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Require last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')   
    is_edit = forms.ChoiceField(label='Role',choices=role_choices, widget=forms.RadioSelect(),initial=False)
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','phone_number','is_edit')
    def __init__(self, *args, **kwargs):
       super(AddForm, self).__init__(*args, **kwargs)
       del self.fields['password1']
       del self.fields['password2']
