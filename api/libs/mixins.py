# python imports
import csv
from io import StringIO
from pytz import timezone
from datetime import datetime
import logging

# django imports
from django.db.models.fields import BooleanField, SmallIntegerField, IntegerField
from django.conf import settings
from django.db import transaction
# from django.contrib import messages

logger = logging.getLogger(__name__)


class RemoveDeleteOptionMixin(object):
    """
    Mixin to Remove delete options from admin
    """

    def has_delete_permission(self, request, obj=None):
        """
        This removes the option to delete a model instance
        """
        return False


class CSVImportMixin(object):
    """
    """
    @transaction.atomic
    def import_csv(self, files):
        # generate validated data for all object in csv
        validated_data_list = []

        # read csv file
        reader = csv.reader(
            files['csv'].read().decode('utf-8').splitlines()
        )

        # validate header
        header = next(reader)
        success = self._validate_header(header, self.csv_template_header)
        if success is False:
            return False, "Invalid template format for header"

        # validate data
        line_number = 1
        for line in reader:
            line_number += 1
            success, response = self._validate_data(header, line)
            if success is False:
                return (
                    False, "Line {line}: {response}".format(line=line_number, response=response)
                )
            validated_data_list.append(response)

        # insert data
        for validated_data in validated_data_list:
            self.model.objects.create(**validated_data)

        # return response
        return True, "All {obj} uploaded successfully".format(obj=self.model._meta.model_name)

    def _validate_header(self, header, template_header):
        return header == template_header

    def _validate_data(self, header, line):
        if len(header) != len(line):
            return False, "Invalid data"
        _validate_data_map = dict(zip(header, line))

        fields = self.model._meta.fields
        fields_map = dict(
            (field.attname, field)
            for field in fields
        )

        # validate all attr in a header
        for attr in header:
            field = fields_map[attr]

            if field.validators:
                try:
                    data = _validate_data_map[attr]
                    if field.__class__ in [SmallIntegerField, IntegerField]:
                        data = int(data)
                    field.run_validators(data)
                except Exception:
                    return False, "Inavlid validation for {field}".format(field=attr)

            if field.unique:
                if self.model.objects.filter(**{attr: _validate_data_map[attr]}).exists():
                    return False, "Already Exist"

            if field.choices:
                if not (int(_validate_data_map[attr]) in field.choices):
                    return False, "Invalid choices for {field}".format(field=attr)

            if field.is_relation:
                if not field.related_model.objects.filter(
                    **{"id": _validate_data_map[attr]}
                ).exists():
                    return False, "{field} not exist".format(field=attr)

            if type(field) == BooleanField:
                if int(_validate_data_map[attr]) not in [0, 1]:
                    return False, "{field} choices are: {choices}".format(
                        field=attr, choices="0, 1"
                    )

            if field.blank is False and _validate_data_map[attr] == '':
                return False, "Invalid data for {field}".format(field=attr)

        # check if unique constraint field already exist
        return True, _validate_data_map


class CSVDownloadMixin(object):
    """
    """
    # Add custom fields in extra_download_fields
    extra_download_fields = list()

    # Add fields to be excluded in exclude_download_fields
    exclude_download_fields = list()

    def createCSV(self, queryset):
        """
        This method returns a csv file
        """
        f = StringIO()
        writer = csv.writer(f)
        headers = list()

        for field in queryset.model._meta.fields:
            headers.append(field.name)

        if len(self.exclude_download_fields) > 0:
            headers = list(set(headers)-set(self.exclude_download_fields))

        # to maintain the order of fields
        headers.sort()

        headers += self.extra_download_fields
        my_timezone = timezone(settings.TIME_ZONE)

        writer.writerow(headers)
        for obj in queryset:
            row = list()
            for field in headers[0:len(headers)-len(self.extra_download_fields)]:
                field_obj = queryset.model._meta.get_field(field)
                val = getattr(obj, field)

                if isinstance(val, datetime):
                    # changing timezone to local time
                    val = val.astimezone(my_timezone)

                if len(field_obj.choices) > 0:
                    # changing value of choice fields
                    # String value for gender comes as ''
                    if val is None or val == '':
                        val = 'N/A'
                    else:
                        val = field_obj.choices[val]

                if callable(val):
                    val = val()

                if type(val) == str:
                    val = val.encode("utf-8")

                try:
                    row.append(val.decode("utf-8"))
                except AttributeError:
                    row.append(val)
            row = self.add_extra_headers(row, obj)
            writer.writerow(row)

        f.seek(0)
        return f

    def customCSV(self, response):
        f = StringIO()
        writer = csv.writer(f)
        headers = list()
        if len(response) > 0:
            headers = response[0].keys()
            writer.writerow(headers)
            for obj in response:
                row = list()
                for fields in headers:
                    row.append(obj[fields])
                writer.writerow(row)
            f.seek(0)
        return f

    def add_extra_headers(self, row, obj):
        """
        This method must be implement if specifying extra fields during download
        """
        raise NotImplementedError('add_extra_headers() method must be implemented')


class MarkActiveInactiveMixin(object):
    """
    Mixin to add inactive action
    """
    def set_inactive(self, request, queryset):
        """
        This action marks selected units inactive
        """
        queryset.update(is_active=False)
    set_inactive.short_description = "Mark as Inactive"

    def set_active(self, request, queryset):
        """
        This action marks selected units inactive
        """
        queryset.update(is_active=True)
    set_active.short_description = "Mark as Active"
