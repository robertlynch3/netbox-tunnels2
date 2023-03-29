"""Django views for network tunnels.

(c) 2020 Justin Drew
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from django.contrib.auth.mixins import PermissionRequiredMixin

from netbox.views.generic import BulkDeleteView, BulkImportView, ObjectEditView, ObjectListView, ObjectView

from . import forms, models, tables, filtersets

class TunnelView(PermissionRequiredMixin, ObjectView):
    permission_required = "netbox_tunnels2.view_tunnels"
    queryset = models.Tunnel.objects.all()

class ListTunnelView(PermissionRequiredMixin, ObjectListView):
    """View for listing all Tunnels."""

    permission_required = "netbox_tunnels2.view_tunnels"
    model = models.Tunnel
    queryset = models.Tunnel.objects.all().order_by("id")
    filterset = filtersets.TunnelFilterSet
    filterset_form = forms.TunnelFilterForm
    table = tables.TunnelTable
    


class CreateTunnelView(PermissionRequiredMixin, ObjectEditView):
    """View for creating a new Tunnels."""

    permission_required = "netbox_tunnels2.add_tunnels"
    model = models.Tunnel
    queryset = models.Tunnel.objects.all()
    form = forms.TunnelCreationForm
    default_return_url = "plugins:netbox_tunnels2:tunnel_list"


class BulkDeleteTunnelView(PermissionRequiredMixin, BulkDeleteView):
    """View for deleting one or more Tunnels."""

    permission_required = "netbox_tunnels2.delete_tunnels"
    queryset = models.Tunnel.objects.filter()
    table = tables.TunnelTable
    default_return_url = "plugins:netbox_tunnels2:tunnel_list"

