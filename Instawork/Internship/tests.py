from django.test import TestCase

# Create your tests here.
class CreateTeams(TestCase):
    def setUp(self):
        Profile.objects.create()
