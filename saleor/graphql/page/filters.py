import django_filters
from django.db.models import Q
from graphene_django.filter import GlobalIDMultipleChoiceFilter

from ...page.models import Page
from ..core.filters import MetadataFilterBase
from ..core.types import FilterInputObjectType
from ..utils import resolve_global_ids_to_primary_keys
from .types import PageType


def filter_page_search(qs, _, value):
    if not value:
        return qs
    return qs.filter(
        Q(title__trigram_similar=value)
        | Q(slug__trigram_similar=value)
        | Q(content__icontains=value)
    )


def filter_page_page_types(qs, _, value):
    if not value:
        return qs
    _, page_types_pks = resolve_global_ids_to_primary_keys(value, PageType)
    return qs.filter(page_type_id__in=page_types_pks)


def filter_page_type_search(qs, _, value):
    if not value:
        return qs
    return qs.filter(Q(name__trigram_similar=value) | Q(slug__trigram_similar=value))


class PageFilter(MetadataFilterBase):
    search = django_filters.CharFilter(method=filter_page_search)
    page_types = GlobalIDMultipleChoiceFilter(field_name="page_type")

    class Meta:
        model = Page
        fields = ["search"]


class PageFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = PageFilter


class PageTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_page_type_search)


class PageTypeFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = PageTypeFilter
