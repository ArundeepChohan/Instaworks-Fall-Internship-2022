from django.test import TestCase, Client
from django.urls import reverse

from .models import Profile, Team
from .forms import ProfileForm
# Create your tests here.
 
class Instawork(TestCase):

    #fields are first_name, last_name, is_edit, email
    def setUp(self):
        self.client = Client()
        self.user = Profile.objects.create(first_name='A', last_name='C',email='a@hotmail.com',is_edit=True,phone_number="+17783711066")
        self.user.set_password('password')
        self.user.save()
        self.login_url =  reverse('login')
        self.add_url = reverse('add')

    def test_first_name_label(self):
        author = self.user
        field_label = author._meta.get_field('first_name').verbose_name
        #print(field_label)
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        author = self.user
        max_length = author._meta.get_field('first_name').max_length
        #print(max_length)
        self.assertEqual(max_length, 100)

    def test_last_name_label(self):
        author = self.user
        field_label = author._meta.get_field('last_name').verbose_name
        #print(field_label)
        self.assertEqual(field_label, 'last name')

    def test_last_name_max_length(self):
        author = self.user
        max_length = author._meta.get_field('last_name').max_length
        #print(max_length)
        self.assertEqual(max_length, 100)

    def test_email_label(self):
        author = self.user
        field_label = author._meta.get_field('email').verbose_name
        #print(field_label)
        self.assertEqual(field_label, 'email address')

    def test_email_max_length(self):
        author = self.user
        max_length = author._meta.get_field('email').max_length
        #print(max_length)
        self.assertEqual(max_length, 254)

    def test_is_edit_label(self):
        author = self.user
        field_label = author._meta.get_field('is_edit').verbose_name
        #print(field_label)
        self.assertEqual(field_label, 'is edit')

    def test_phone_number_max_length(self):
        author = self.user
        max_length = author._meta.get_field('phone_number').max_length
        #print(max_length)
        self.assertEqual(max_length, 25)

    def test_phone_number_label(self):
        author = self.user
        field_label = author._meta.get_field('phone_number').verbose_name
        #print(field_label)
        self.assertEqual(field_label, 'phone number')

    def test_create_new_team_for_user(self):
        author = self.user
        if author.team is None:
            new_team = Team()
            new_team.save()
            author.team=new_team
            author.save()
        #print(author.team)
        self.assertEqual(author.team,new_team)

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"home.html")
    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"login.html") 
    def test_login(self):
        user_login = self.client.post(self.login_url, {'email': self.user.email, 'password': self.user.password})
        #self.assertTrue(user_login.context['user'].is_authenticated)
        self.assertTemplateUsed(user_login,"home.html")
    def test_get_add_page(self):
        response=self.client.post(self.login_url, {'email': self.user.email, 'password': self.user.password})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"add.html")
    def test_form_email_duplicate_validity(self):
        form_data = {
            'email': 'a@hotmail.com',
        }
        form = ProfileForm(data=form_data)
        self.assertIn('email', form.errors)
        print(form.errors['email'])
        self.assertTrue(form.errors['email'],['User with this Email address already exists.'])
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
            'first_name':'c',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('first_name', form.errors)

    def test_form_last_name_validity(self):
        form_data = {
            'last_name':'a',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('last_name', form.errors)

    def test_form_last_name_validity(self):
        form_data = {
            'phone_number':'+17783711066',
        }
        form = ProfileForm(data=form_data)
        self.assertNotIn('phone_number', form.errors)


