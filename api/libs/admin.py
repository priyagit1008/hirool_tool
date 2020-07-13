
# django imports
from django.contrib import admin
# from django.contrib.admin import helpers
# from django.template.response import TemplateResponse
# from django.contrib import messages

# third party imports
from rest_framework.authtoken.models import Token
# from rest_framework.exceptions import ValidationError

# app level imports
from .mixins import (
    RemoveDeleteOptionMixin,
    MarkActiveInactiveMixin,
)

# remove token from admin panel
admin.site.unregister(Token)


class MyAbstractBaseModelAdmin(RemoveDeleteOptionMixin, admin.ModelAdmin):
    """
    Abstract base class based on ModelAdmin
    """
    ordering = ('-id', )
    show_full_result_count = False

    def get_actions(self, request):
        """
        This removes the option to delete selected instances
        """
        actions = super(MyAbstractBaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class MyModelAdmin(MarkActiveInactiveMixin, MyAbstractBaseModelAdmin):
    """
    Base admin class with active/inactive actions
    """
    actions = ('set_active', 'set_inactive')
