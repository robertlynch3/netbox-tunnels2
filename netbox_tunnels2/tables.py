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
from .models import PluginTunnel, TunnelType


COL_SIDE_A_HOST_ASSIGNMENT = """
    {% if record.side_a_assigned_object.device %}
    <a href="{{ record.side_a_assigned_object.device.get_absolute_url }}">{{ record.side_a_assigned_object.device|placeholder }}</a>
    {% else %}
    <a href="{{ record.side_a_assigned_object.virtual_machine.get_absolute_url }}">{{ record.side_a_assigned_object.virtual_machine|placeholder }}</a>
    {% endif %}
 """
COL_SIDE_B_HOST_ASSIGNMENT = """
    {% if record.side_b_assigned_object.device %}
    <a href="{{ record.side_b_assigned_object.device.get_absolute_url }}">{{ record.side_b_assigned_object.device|placeholder }}</a>
    {% else %}
    <a href="{{ record.side_b_assigned_object.virtual_machine.get_absolute_url }}">{{ record.side_b_assigned_object.virtual_machine|placeholder }}</a>
    {% endif %}
 """


class RelatedTunnelTable(NetBoxTable):
    """Table for displaying Tunnel instances related to an interface."""
    name = tables.Column(
        linkify=True
    )
    tunnel_type = tables.Column(linkify=True)
    b_pub_address = tables.Column(linkify=True)
    status = ChoiceFieldColumn()
    tenant = tables.Column(linkify=True)

    side_b_host = tables.TemplateColumn(
        template_code=COL_SIDE_B_HOST_ASSIGNMENT,
        verbose_name="Side B Host",
    )
    side_b_assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Side B Interface",
    )

    class Meta(NetBoxTable.Meta):
        """Class to define what is used for interface_extend.html template to show
        tunnels related to an interface"""

        model = PluginTunnel
        fields = (
            'pk',
            'id',
            "name",
            "tenant",
            "tunnel_type",
            "side_b_host",
            "side_b_assigned_object",
            "status",
            "b_pub_address"
        )
        default_columns = ('name', 'status', 'tunnel_type',
                           'side_b_host', 'b_pub_address')


class TunnelTable(RelatedTunnelTable):
    """Table for displaying configured Tunnel instances."""
    a_pub_address = tables.Column(linkify=True)
    side_a_host = tables.TemplateColumn(
        template_code=COL_SIDE_A_HOST_ASSIGNMENT,
        verbose_name="Side A Host",
    )
    side_a_assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Side A Interface",
    )

    class Meta(RelatedTunnelTable.Meta):
        """Class to define what is used for tunnel_lists.html template to show configured tunnels."""

        RelatedTunnelTable.Meta.fields += (
            "side_a_host",
            "side_a_assigned_object",
            "a_pub_address",
        )
        RelatedTunnelTable.Meta.default_columns += ('side_a_host', 'a_pub_address')


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


