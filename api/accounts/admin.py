from django.contrib import admin
from accounts.users.models import User
from libs.admin import MyAbstractBaseModelAdmin


@admin.register(User)
class UserAdmin(MyAbstractBaseModelAdmin):
    """
    """
    list_display = ('email', 'mobile', 'first_name')
