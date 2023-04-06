"""Plugin additions to the NetBox navigation menu.

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

from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


# tunnel_buttons = [
#     PluginMenuButton(
#         link='plugins:netbox_tunnels2:tunnel_add',
#         title='Add',
#         icon_class='mdi mdi-plus-thick',
#         color=ButtonColorChoices.GREEN,
#         permissions=["netbox_tunnels.add_tunnels"]
#     )
# ]

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_tunnels2:tunnel_list",
        link_text="Tunnels",
        permissions=["netbox_tunnels.view_tunnels"],
        buttons=(PluginMenuButton(
            link='plugins:netbox_tunnels2:tunnel_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_tunnels.add_tunnels"]
        ),)
    ),
    PluginMenuItem(
        link="plugins:netbox_tunnels2:tunneltype_list",
        link_text="Tunnel Types",
        permissions=["netbox_tunnels.view_tunnel_types"],
        buttons=(PluginMenuButton(
            link='plugins:netbox_tunnels2:tunneltype_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_tunnels.add_tunneltype"]
        ),)
    ),
)
