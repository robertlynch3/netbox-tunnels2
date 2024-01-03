import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Interface
from tenancy.models import Tenant
from .models import PluginTunnel, TunnelType


class TunnelFilterSet(NetBoxModelFilterSet):
    side_a_interface = django_filters.ModelMultipleChoiceFilter(
        field_name="interface__name",
        queryset=Interface.objects.all(),
        to_field_name="name",
        label="Side A Interface (name)",
    )
    side_a_interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface",
        queryset=Interface.objects.all(),
        label="Side A Interface (ID)",
    )
    side_b_interface = django_filters.ModelMultipleChoiceFilter(
        field_name="interface__name",
        queryset=Interface.objects.all(),
        to_field_name="name",
        label="Side B Interface (name)",
    )
    side_b_interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface",
        queryset=Interface.objects.all(),
        label="Side B Interface (ID)",
    )
    tenant_id = django_filters.ModelChoiceFilter(
        field_name="tenant_id",
        queryset=Tenant.objects.all(),
        to_field_name="id",
        label="Tenant (ID)",
    )

    class Meta:
        model = PluginTunnel
        fields = (
            "name",
            "status",
            "tunnel_type",
            "a_pub_address",
            "b_pub_address",
            "side_a_interface",
            "side_a_interface_id",
            "side_b_interface",
            "side_b_interface_id",
        )

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)


class TunnelTypeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = TunnelType
        fields = (
            "name",
            "slug"
        )
