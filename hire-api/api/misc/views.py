# django/rest_framework imports
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging

# app level imports
from .models import APIConfig
# from libs.constants import BAD_REQUEST
# from libs.exceptions import ParseException

# third party imports
from reversion.models import Version


logger = logging.getLogger(__name__)


@login_required(login_url=settings.ADMIN_LOGIN_URL)
def show_reversion_changes(request, id, *args, **kwargs):
    try:
        cur_version = Version.objects.get(id=id)
        current_data = cur_version.field_dict

        # get the previous version
        last_version = cur_version.content_type.version_set.filter(
            revision__date_created__lt=cur_version.revision.date_created,
            object_id=cur_version.field_dict['id']
        )[:1]

        if last_version:
            old_data = last_version[0].field_dict
        else:
            old_data = current_data

        return render(
            request,
            'reversion_changes.html',
            {
                'fields': current_data.keys(),
                'old': old_data,
                'current': current_data,
            },
        )

    except Exception:
        logger.error(
            "Unable to retrieve cur_version/last_version ",
            exc_info=True
        )


class APIConfViewSet(ViewSet):
    """
    """
    authentication_classes = (TokenAuthentication,)

    @action(methods=['get'], detail=False)
    def init(self, request):
        """
        This view returns API configuration.
        """
        # try:
        #     app_version = int(request.META['HTTP_X_APP_VERSION'])
        # except KeyError:
        #     raise ParseException(BAD_REQUEST, errors="X-APP-VERSION header is missing.")

        apiconfig_data = APIConfig.get_init_data()
        # app_version_status = APIConfig.get_app_version_status(apiconfig_data, "11")

        return Response(apiconfig_data)

    @action(methods=['get'], detail=False, url_path='health-check')
    def health_check(self, request):
        """
        This view returns health check response for EC2 reachbility.
        """
        return Response({"detail": "EC2 is up and running."})
