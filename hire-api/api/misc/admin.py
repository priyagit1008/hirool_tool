# python imports
import logging

# django imports
from django.contrib import admin
# from django.utils.html import format_html
# from django.urls import reverse

# third party imports
# from reversion.models import Version
# from reversion.admin import VersionAdmin

# project level imports
from libs.admin import MyAbstractBaseModelAdmin
# from libs.mixins import (
#     RemoveAddOptionMixin,
#     RemoveDeleteOptionMixin
# )

# app level imports
from .models import APIConfig


logger = logging.getLogger(__name__)


@admin.register(APIConfig)
class APIConfigAdmin(MyAbstractBaseModelAdmin):
    """
    """
    list_display = ('key', 'usage_type', 'real_value', 'text_value')
    search_fields = ('key', 'value', 'text_value')
    list_filter = ('usage_type',)

    def real_value(self, obj):
        if obj.key == 'iot_seed_values':
            """
            show only 10 values here
            """
            if len(obj.value) > 10:
                return obj.value[:10]
            else:
                return obj.value
        else:
            return obj.value
