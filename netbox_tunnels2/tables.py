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
from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import Tunnel


class TunnelTable(NetBoxTable):
    """Table for displaying configured Tunnel instances."""
    name = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    
    class Meta(NetBoxTable.Meta):
        """Class to define what is used for tunnel_lists.html template to show configured tunnels."""

        model = Tunnel
        fields = (
            'pk',
            'id',
            "name",
            "status",
            "tunnel_type",
            "src_address",
            "dst_address"
        )
        default_columns = ('name', 'status', 'tunnel_type', 'src_address', 'dst_address')

