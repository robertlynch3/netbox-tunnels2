"""Plugin declaration for netbox_tunnels.
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

from extras.plugins import PluginConfig


class TunnelsConfig(PluginConfig):
    """This class defines attributes for the NetBox Tunnels Plugin."""

    name = "netbox_tunnels"
    verbose_name = "Tunnels"
    description = "Netbox Tunnels"
    version = "0.2.3"
    base_url = "tunnels"
    author = "Justin Drew"
    author_email = "***REMOVED***"
    required_settings = []
    # default_settings = {}
    # caching_config = {}


config = TunnelsConfig
