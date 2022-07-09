from django.test import TestCase, Client
from django.urls import reverse

from .models import Profile, Team
from .forms import ProfileForm
# Create your tests here.


class Instawork(TestCase):

    # fields are first_name, last_name, is_edit, email
    def setUp(self):
        self.client = Client()
        self.user = Profile.objects.create(
            first_name='A', last_name='C', email='a@hotmail.com', is_edit=True, phone_number="+17783711066")
        self.user.set_password('password')
        self.user.save()
        self.login_url = reverse('login')
        self.add_url = reverse('add')
        self.home_url = reverse('home')

    def test_label(self,label='',value=''):
        author = self.user
        try:
            field_label = author._meta.get_field(label).verbose_name
            # print(field_label)
            self.assertEqual(field_label, value)
        except:
            self.assertFalse(True)

        
    def test_max_length(self,label='',value=''):
        author = self.user
        try:
            max_length = author._meta.get_field(label).max_length
            # print(max_length)
            self.assertEqual(max_length, value)
        except:
            self.assertFalse(True)
        

    def test_first_name_label(self):
        self.test_label('first_name','first name')

    def test_first_name_max_length(self):
        self.test_max_length('first_name',100)   

    def test_last_name_label(self):
        self.test_label('last_name','last name')

    def test_last_name_max_length(self):
        self.test_max_length('last_name',100)

    def test_email_label(self):
        self.test_label('email','email address')

    def test_email_max_length(self):
        self.test_max_length('email',254)

    def test_is_edit_label(self):
        self.test_label('is_edit','is edit')

    def test_phone_number_label(self):
        self.test_label('phone_number','phone number')

    def test_phone_number_max_length(self):
        self.test_max_length('phone_number',25)

    def test_create_new_team_for_user(self):
        author = self.user
        if author.team is None:
            new_team = Team()
            new_team.save()
            author.team = new_team
            author.save()
        # print(author.team)
        self.assertEqual(author.team, new_team)

    def test_page(self,url='',template=''):
        try:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
        except:
            self.assertFalse(True)

    def test_get_home_page(self):
        self.test_page(self.home_url,"home.html")

    def test_get_login_page(self):
        self.test_page(self.login_url,"login.html")

    def test_get_admin_page(self):
        pass

    def test_get_add_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.add_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add.html")

    def test_login(self):
        self.client.force_login(self.user)
        response = self.client.get(self.home_url, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, "home.html")


    def test_get_edit_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit.html")

    def test_form_email_duplicate_validity(self):
        form_data = {
            'email': 'a@hotmail.com',
        }
        form = ProfileForm(data=form_data)
        self.assertIn('email', form.errors)
        print(form.errors['email'])
        self.assertTrue(form.errors['email'], [
                        'User with this Email address already exists.'])

    def test_form_email_validity(self):
        form_data = {
            'email': 'b@hotmail.com',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('email', form.errors)

    def test_form_is_edit_validity(self):
        form_data = {
            'is_edit': True,
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('is_edit', form.errors)

    def test_form_first_name_validity(self):
        form_data = {
            'first_name': 'c',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('first_name', form.errors)

    def test_form_last_name_validity(self):
        form_data = {
            'last_name': 'a',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('last_name', form.errors)

    def test_form_last_name_validity(self):
        form_data = {
            'phone_number': '+17783711066',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('phone_number', form.errors)