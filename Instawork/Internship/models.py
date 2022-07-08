from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from .managers import CustomUserManager

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Profile(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True) # Here
    first_name = models.TextField(max_length=100, blank=True,null=True)
    last_name = models.TextField(max_length=100, blank=True,null=True)
    phone_number = PhoneNumberField(max_length=25, region='US')
    is_edit = models.BooleanField(default=False)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True, blank=True, default = None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    

