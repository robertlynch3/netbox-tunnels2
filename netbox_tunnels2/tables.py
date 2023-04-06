"""Tables for displaying list of configured Tunnels.

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
import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from .models import Tunnel, TunnelType


class TunnelTable(NetBoxTable):
    """Table for displaying configured Tunnel instances."""
    name = tables.Column(
        linkify=True
    )
    tunnel_type=tables.Column(linkify=True)
    local_address = tables.Column(linkify=True)
    remote_address = tables.Column(linkify=True)
    status = ChoiceFieldColumn()
    
    class Meta(NetBoxTable.Meta):
        """Class to define what is used for tunnel_lists.html template to show configured tunnels."""

        model = Tunnel
        fields = (
            'pk',
            'id',
            "name",
            "tunnel_type",
            "status",
            "local_address",
            "remote_address"
        )
        default_columns = ('name', 'status', 'tunnel_type', 'local_address', 'remote_address')

class TunnelTypeTable(NetBoxTable):
    """Table for displaying configured Tunnel instances."""
    name = tables.Column(
        linkify=True
    )
    tunnel_count=columns.LinkedCountColumn(
        viewname='plugins:netbox_tunnels2:tunnel_list',
        url_params={'tunnel_type': 'pk'},
        verbose_name='Tunnels'
    )
    class Meta(NetBoxTable.Meta):
        """Class to define what is used for tunnel_lists.html template to show configured tunnels."""

        model = TunnelType
        fields = (
            'pk',
            'id',
            "name",
            "tunnel_count",
            "slug"
        )
        default_columns = ('name','tunnel_count',)


