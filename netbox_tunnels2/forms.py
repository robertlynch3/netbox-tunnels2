"""Forms for tunnel creation.

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

from django.forms import (
    CharField,
    ChoiceField,
    MultipleChoiceField,
    ChoiceField,
    PasswordInput
)

from utilities.forms import (
    DynamicModelChoiceField
)

from dcim.models import Device

from netbox.forms import NetBoxModelForm, NetBoxModelBulkEditForm, NetBoxModelFilterSetForm

from .models import Tunnel, TunnelStatusChoices, TunnelTypeChoices


class TunnelCreationForm(NetBoxModelForm):
    """Form for creating a new tunnel."""

    name = CharField(required=True, label="Name", help_text="Name of tunnel")

    status = ChoiceField(
            choices=TunnelStatusChoices,
            required=False
        )

    tunnel_type = ChoiceField(
        choices=TunnelTypeChoices.CHOICES,
        required=True,
        label="Tunnel type",
        help_text="Tunnel type. This must be specified.",
    )

    src_address = CharField(required=True, label="Source IP address", help_text="IP address of the source device")

    dst_address = CharField(required=True, label="Peer IP address", help_text="IP address of the peer device")

    psk = CharField(
        required=False, label="Pre-shared Key", widget=PasswordInput, help_text="Pre-shared key"
    )

    class Meta:
        """Class to define what is used to create a new network tunnel."""

        model = Tunnel
        fields = (
            "name",
            "status",
            "tunnel_type",
            "src_address",
            "dst_address",
            "psk",
            'comments',
            'tags',
        )


class TunnelFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Tunnel instances."""
    model = Tunnel

    #device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)

    status = MultipleChoiceField(choices=TunnelStatusChoices, required=False)
    tunnel_type =  MultipleChoiceField(choices=TunnelTypeChoices, required=False)

    #q = MultipleChoiceField(required=False, label="Search")

    class Meta:
        """Class to define what is used for filtering tunnels with the search box."""

        model = Tunnel
        fields = (
            "src_address",
            "dst_address",
            "psk",
            "tunnel_type",
        )

