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
    PasswordInput,
    ModelChoiceField
)

from utilities.forms import (
    DynamicModelChoiceField,
    SlugField
)

from dcim.models import Device
from ipam.models import IPAddress, VRF
from ipam.formfields import IPNetworkFormField
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError

from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm

from .models import Tunnel, TunnelStatusChoices, TunnelType

class TunnelEditForm(NetBoxModelForm):
    """Form for creating a new tunnel."""

    name = CharField(required=True, label="Name", help_text="Name of tunnel")

    status = ChoiceField(
            choices=TunnelStatusChoices,
            required=False
        )

    tunnel_type = ModelChoiceField(
            queryset=TunnelType.objects.all(),
            required=True
    )

    local_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        query_params={
            'device_id': '$device'
        }
    )
    remote_VRF = DynamicModelChoiceField(label='Remote Address VRF', queryset=VRF.objects.all(),required=False)
    remote_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        query_params={
            'device_id': '$remote_VRF'
        },
        required=False
    )
    psk = CharField(required=False, label="Pre-shared Key", widget=PasswordInput, help_text="Pre-shared key")

    class Meta:
        """Class to define what is used to create a new network tunnel."""

        model = Tunnel
        fields = (
            "name",
            "status",
            "tunnel_type",
            "local_address",
            "remote_address",
            "psk",
            'comments',
            'tags',
        )
class TunnelAddForm(TunnelEditForm):
    tunnel_type = ModelChoiceField(
            queryset=TunnelType.objects.all(),
            required=True
    )
    remote_VRF = DynamicModelChoiceField(label='Remote Address VRF', queryset=VRF.objects.all(),required=False)
    remote_address = IPNetworkFormField(required=True)

    fields = (
            "name",
            "status",
            "tunnel_type",
            "local_address",
            "remote_VRF",
            "remote_address",
            "psk",
            "comments",
            "tags",
        )
    field_order = ["name",
            "status",
            "tunnel_type",
            "local_address",
            "remote_VRF",
            "remote_address",
            "psk",
            "comments",
            "tags"]
    
    def clean_remote_address(self):
        
        if self.data['remote_VRF']!='':
            vrf=VRF.objects.get(id=self.data['remote_VRF'])
        else:
            vrf=0
        try:
            if vrf==0:
                ip = IPAddress.objects.get(address=str(self.cleaned_data['remote_address']))
            else:
                ip = IPAddress.objects.get(address=str(self.cleaned_data['remote_address']),vrf=vrf)
        except MultipleObjectsReturned:
            if vrf==0:
                ip = IPAddress.objects.filter(address=str(self.cleaned_data['remote_address'])).first()
            else:
                ip = IPAddress.objects.filter(address=str(self.cleaned_data['remote_address']),vrf=vrf).first()
        except ObjectDoesNotExist:
            if vrf==0:
                ip = IPAddress.objects.create(address=str(self.cleaned_data['remote_address']))
            else:    
                ip = IPAddress.objects.create(address=str(self.cleaned_data['remote_address']),vrf=vrf)
        self.cleaned_data['remote_address'] = ip
        return self.cleaned_data['remote_address']
    
class TunnelFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Tunnel instances."""
    model = Tunnel
    status = MultipleChoiceField(choices=TunnelStatusChoices, required=False)
    tunnel_type = tunnel_type = ModelChoiceField(
            queryset=TunnelType.objects.all(),
            required=False
    )
    class Meta:
        """Class to define what is used for filtering tunnels with the search box."""

        model = Tunnel
        fields = (
            "local_address",
            "remote_address",
            "psk",
            "tunnel_type",
        )

#
# Tunnel Type
#

class TunnelTypeEditForm(NetBoxModelForm):
    """Form for creating a new tunnel."""
    slug = SlugField()
    class Meta:
        """Class to define what is used to create a new network tunnel."""
        model = TunnelType
        fields = ('name', 'slug')