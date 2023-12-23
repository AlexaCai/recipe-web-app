from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from recipes.models import Recipe

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    search_fields = ['email']
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['id', 'full_name', 'email', 'timestamp', 'admin']
    list_filter = ['admin', 'staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('id', 'full_name', 'email', 'password', 'timestamp')}),
        ('Favorite and created recipes', {'fields': ('favorite_recipes', 'user_created_recipes')}),
        ('Permissions', {'fields': ('admin','staff','is_active')}),
    )

    readonly_fields = ['id', 'full_name', 'email', 'password', 'timestamp']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email', 'full_name',]
    ordering = ['email']
    filter_horizontal = ()

    # Used to display the favorite and created recipes for each user in Django admin interface
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields['favorite_recipes'].queryset = Recipe.objects.filter(favorites=obj)
            form.base_fields['user_created_recipes'].queryset = Recipe.objects.filter(user=obj)
        return form

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)