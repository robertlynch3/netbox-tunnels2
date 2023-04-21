from django.contrib.auth.mixins import PermissionRequiredMixin
from utilities.utils import count_related

from netbox.views.generic import BulkDeleteView, BulkImportView, ObjectEditView, ObjectListView, ObjectView, ObjectDeleteView

from . import forms, models, tables, filtersets

class TunnelView(PermissionRequiredMixin, ObjectView):
    permission_required = "netbox_tunnels2.view_tunnel"
    queryset = models.Tunnel.objects.all()

class ListTunnelView(PermissionRequiredMixin, ObjectListView):
    """View for listing all Tunnels."""

    permission_required = "netbox_tunnels2.view_tunnel"
    model = models.Tunnel
    queryset = models.Tunnel.objects.all().order_by("id")
    filterset = filtersets.TunnelFilterSet
    filterset_form = forms.TunnelFilterForm
    table = tables.TunnelTable
    

class EditTunnelView(PermissionRequiredMixin, ObjectEditView):
    """View for creating a new Tunnels."""

    permission_required = "netbox_tunnels2.change_tunnel"
    model = models.Tunnel
    queryset = models.Tunnel.objects.all()
    form = forms.TunnelEditForm
    default_return_url = "plugins:netbox_tunnels2:tunnel_list"
    template_name = "netbox_tunnels2/tunnel_edit.html"

class CreateTunnelView(PermissionRequiredMixin, ObjectEditView):
    """View for creating a new Tunnels."""
    permission_required = "netbox_tunnels2.add_tunnel"
    model = models.Tunnel
    queryset = models.Tunnel.objects.all()
    #form = forms.TunnelAddForm
    form = forms.TunnelEditForm
    default_return_url = "plugins:netbox_tunnels2:tunnel_list"
    template_name = "netbox_tunnels2/tunnel_edit.html"

class DeleteTunnelView(PermissionRequiredMixin,ObjectDeleteView):
    permission_required = "netbox_tunnels2.delete_tunnel"
    queryset = models.Tunnel.objects.all()
    default_return_url = "plugins:netbox_tunnels2:tunnel_list"

class BulkDeleteTunnelView(PermissionRequiredMixin, BulkDeleteView):
    """View for deleting one or more Tunnels."""

    permission_required = "netbox_tunnels2.delete_tunnel"
    queryset = models.Tunnel.objects.filter()
    table = tables.TunnelTable
    default_return_url = "plugins:netbox_tunnels2:tunnel_list"



#
# Tunnel Type
#

class TunnelTypeView(PermissionRequiredMixin, ObjectView):
    permission_required = "netbox_tunnels2.view_tunneltype"
    queryset = models.TunnelType.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.TunnelTable(instance.tunnels.all())
        table.configure(request)
        return {
            'tunnel_table': table,
        }

class ListTunnelTypeView(PermissionRequiredMixin, ObjectListView):
    """View for listing all Tunnels."""
    permission_required = "netbox_tunnels2.view_tunneltype"
    model = models.TunnelType
    queryset = models.TunnelType.objects.annotate(tunnel_count=count_related(models.Tunnel,'tunnel_type'))
    table = tables.TunnelTypeTable
    

class EditTunnelTypeView(PermissionRequiredMixin, ObjectEditView):
    """View for creating a new Tunnels."""

    permission_required = "netbox_tunnels2.change_tunneltype"
    model = models.TunnelType
    queryset = models.TunnelType.objects.all()
    form = forms.TunnelTypeEditForm
    default_return_url = "plugins:netbox_tunnels2:tunneltype_list"

class CreateTunnelTypeView(PermissionRequiredMixin, ObjectEditView):
    """View for creating a new Tunnels."""

    permission_required = "netbox_tunnels2.add_tunneltype"
    model = models.TunnelType
    queryset = models.TunnelType.objects.all()
    form = forms.TunnelTypeEditForm
    default_return_url = "plugins:netbox_tunnels2:tunneltype_list"
    
class DeleteTunnelTypeView(PermissionRequiredMixin,ObjectDeleteView):
    permission_required = "netbox_tunnels2.delete_tunneltype"
    queryset = models.TunnelType.objects.all()
    default_return_url = "plugins:netbox_tunnels2:tunneltype_list"


class BulkDeleteTunnelTypeView(PermissionRequiredMixin, BulkDeleteView):
    """View for deleting one or more Tunnels."""

    permission_required = "netbox_tunnels2.delete_tunneltype"
    queryset = models.TunnelType.objects.filter()
    table = tables.TunnelTable
    default_return_url = "plugins:netbox_tunnels2:tunneltype_list"
