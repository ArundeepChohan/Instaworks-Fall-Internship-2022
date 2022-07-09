from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ProfileForm
from .models import Profile


class CustomUserAdmin(UserAdmin):
    add_form = ProfileForm
    model = Profile
    list_display = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'is_edit', 'team')
    ordering = ('email',)
    readonly_fields = ('username',)
    pass

admin.site.register(Profile, CustomUserAdmin)
# Maybe rework this later for better inclusion of all models.

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
