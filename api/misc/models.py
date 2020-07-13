# python imports
import logging

# django and rest_framework imports
from django.db import models
from django.contrib.postgres.fields import JSONField
# from django.utils import timezone
# from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from django.utils.translation import gettext_lazy as _

# third party imports
from model_utils import Choices

# project level imports
from libs.models import TimeStampedModel

# app level imports
# from .constants import (
#     NO_APP_UPDATE_REQUIRED,
#     FORCE_APP_UPDATE_REQUIRED,
#     NORMAL_APP_UPDATE_REQUIRED,
# )


logger = logging.getLogger(__name__)


class APIConfig(TimeStampedModel):
    """
    Configuration Model
    """
    USAGE_TYPES = Choices(
        ('celery', 'celery', 'CELERY'),
        ('init', 'init', 'INIT'),
    )
    key = models.CharField(max_length=128)
    usage_type = models.CharField(max_length=16, choices=USAGE_TYPES)
    value = JSONField(null=True, blank=True)
    text_value = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        app_label = 'misc'
        db_table = 'api_config'
        verbose_name = "APIConfig"
        verbose_name_plural = "APIConfig's"

    def __str__(self):
        return self.key

    def clean(self):
        """
        This method is used to validate the input given for API Config
        """
        pass

    @classmethod
    def get_init_data(cls):
        init_objects = cls.objects.filter(usage_type__iexact='init')
        apiconfig_data = {}
        for row in init_objects:
            data = {
                "value": row.value,
                "text_value": row.text_value
            }
            apiconfig_data[row.key] = data
        return apiconfig_data
