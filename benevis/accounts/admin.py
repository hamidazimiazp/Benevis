from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
from .forms import UserChangeForm
from .models import User
from .models import Profile
from .models import Relation
from django.contrib.auth.models import Group



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
		('Main', {'fields':('username', 'email', 'password')}),
		('Personal info', {'fields':('is_active',)}),
		('Permissions', {'fields':('is_admin',)})
	)

    add_fieldsets = (
		(None, {
			'fields':('username', 'email', 'password1', 'password2')
		}),
	)

    search_fields = ('email', "username")
    ordering = ("username",)
    filter_horizontal = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  readonly_fields = ('image_tag',)

  fields = [("user"),
            ("first_name", "last_name"),
            ("avatar", "image_tag"),
            ("bio"),
            ("age", "phone")]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
  pass