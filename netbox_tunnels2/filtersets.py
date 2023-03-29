"""Filtering logic for Tunnel instances.

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

# import django_filters
# from django.db.models import Q


from netbox.filtersets import NetBoxModelFilterSet
from .models import Tunnel


class TunnelFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Tunnel
        fields = (
            "name",
            "status",
            "tunnel_type",
            "src_address",
            "dst_address"
        )
    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
