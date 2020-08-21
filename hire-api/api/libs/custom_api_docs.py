# django/drf imports
from django.conf.urls import url
from django.urls import include
from django.contrib.auth.decorators import login_required
from rest_framework.settings import api_settings
from rest_framework.documentation import get_docs_view, get_schemajs_view
from rest_framework.schemas import SchemaGenerator


def include_docs_urls(
        title=None, description=None, schema_url=None, public=True,
        patterns=None, generator_class=SchemaGenerator,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
        permission_classes=api_settings.DEFAULT_PERMISSION_CLASSES,
        renderer_classes=None):
    """
    Overriding default include_docs_urls provided by DRF to secure
    the documentation URLs.
    """
    docs_view = get_docs_view(
        title=title,
        description=description,
        schema_url=schema_url,
        public=public,
        patterns=patterns,
        generator_class=generator_class,
        authentication_classes=authentication_classes,
        renderer_classes=renderer_classes,
        permission_classes=permission_classes,
    )
    schema_js_view = get_schemajs_view(
        title=title,
        description=description,
        schema_url=schema_url,
        public=public,
        patterns=patterns,
        generator_class=generator_class,
        authentication_classes=authentication_classes,
        permission_classes=permission_classes,
    )
    urls = [
        url(r'^$', login_required(docs_view), name='docs-index'),
        url(r'^schema.js$', login_required(schema_js_view), name='schema-js')
    ]
    return include((urls, 'api-docs'), namespace='api-docs')
