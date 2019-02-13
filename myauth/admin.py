from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

UserAdmin.list_display = ('username', 'email', 'last_login', 'date_joined', 'is_active', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)