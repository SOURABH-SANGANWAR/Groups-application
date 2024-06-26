from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class MyAdmin(UserAdmin):
    list_display = ('username','email')
    search_fields = ('username','email')
    readonly_fields = ('last_login', 'id',)
    filter_horizontal = ()
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('username', 'email', 'password1', 'password2'),
                },
            ),
        )
    list_filter= ()
    fieldsets = ()

admin.site.register(CustomUser,MyAdmin)