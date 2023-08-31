from django.forms import (
    CharField,
    ChoiceField,
    MultipleChoiceField,
    ChoiceField,
    PasswordInput,
    ModelChoiceField
)

from utilities.forms.fields import (
    DynamicModelChoiceField,
    SlugField,
    DynamicModelMultipleChoiceField
)

from dcim.models import Interface, Device
from ipam.models import IPAddress, VRF
from virtualization.models import VMInterface, VirtualMachine
from ipam.formfields import IPNetworkFormField
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.contrib.contenttypes.models import ContentType

from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from tenancy.models import Tenant

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
    a_pub_VRF = DynamicModelChoiceField(
        label='Side A Address VRF',
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        query_params={
            "tenant_id": "$tenant",
        },
    )
    a_pub_address = DynamicModelChoiceField(
        label='Side A Public IP Address',
        queryset=IPAddress.objects.all(),
        query_params={
            'vrf_id': '$a_pub_VRF',
            'device_id': '$side_a_device',
            'virtual_machine_id': '$side_a_virtual_machine'
        }
    )
    b_pub_VRF = DynamicModelChoiceField(
        label='Side B Address VRF',
        queryset=VRF.objects.all(),
        selector=True,
        required=False
    )
    b_pub_address = DynamicModelChoiceField(
        label='Side B Public IP Address',
        queryset=IPAddress.objects.all(),
        query_params={
            'vrf_id': '$b_pub_VRF',
            'device_id': '$side_b_device',
            'virtual_machine_id': '$side_b_virtual_machine'
        },
        required=False
    )
    psk = CharField(required=False, label="Pre-shared Key", help_text="Pre-shared key")

    side_a_virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        label="Site A VM",
        required=False,
        selector=True,
        query_params={
            "tenant_id": "$tenant",
        },
    )
    side_a_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label="Site A Device",
        required=False,
        selector=True,
        query_params={
            "tenant_id": "$tenant",
        },
    )
    side_a_device_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label="Site A Interface",
        required=False,
        query_params={
            "device_id": "$side_a_device",
        },
    )
    side_a_vm_interface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        label="Site A Interface",
        required=False,
        query_params={
            "virtual_machine_id": "$side_a_virtual_machine",
        },
    )
    side_b_virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        label="Site B VM",
        required=False,
        selector=True,
        query_params={
            "tenant_id": "$tenant",
        },
    )
    side_b_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label="Site B Device",
        required=False,
        selector=True,
    )
    side_b_device_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label="Site B Interface",
        required=False,
        query_params={
            "device_id": "$side_b_device",
        },
    )
    side_b_vm_interface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        label="Site B Interface",
        required=False,
        query_params={
            "virtual_machine_id": "$side_b_virtual_machine",
        },
    )

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {}).copy()
        if instance:
            if type(instance.side_a_assigned_object) is Interface:
                initial["side_a_device_interface"] = instance.side_a_assigned_object
                initial["side_a_device"] = instance.side_a_assigned_object.device
            elif type(instance.side_a_assigned_object) is VMInterface:
                initial["side_a_vm_interface"] = instance.side_a_assigned_object
                initial["side_a_virtual_machine"] = instance.side_a_assigned_object.virtual_machine
            if type(instance.side_b_assigned_object) is Interface:
                initial["side_b_device_interface"] = instance.side_b_assigned_object
                initial["side_b_device"] = instance.side_b_assigned_object.device
            elif type(instance.side_b_assigned_object) is VMInterface:
                initial["side_b_vm_interface"] = instance.side_b_assigned_object
                initial["side_b_virtual_machine"] = instance.side_b_assigned_object.virtual_machine
            if hasattr(instance, 'a_pub_address') and type(instance.a_pub_address) is IPAddress:
                initial["a_pub_VRF"] = instance.a_pub_address.vrf
            if hasattr(instance, 'b_pub_address') and type(instance.b_pub_address) is IPAddress:
                initial["b_pub_VRF"] = instance.b_pub_address.vrf
        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

    class Meta:
        """Class to define what is used to create a new network tunnel."""

        model = Tunnel
        fields = (
            "name",
            "status",
            "tunnel_type",
            "a_pub_address",
            "b_pub_address",
            "psk",
            'comments',
            'tags',
            'tenant',
        )

    def clean(self):
        super().clean()
        error_message = {}
        name = self.cleaned_data['name']
        status = self.cleaned_data['status']
        tunnel_type = self.cleaned_data['tunnel_type']
        a_pub_address = self.cleaned_data['a_pub_address']
        b_pub_address = self.cleaned_data['b_pub_address']
        psk = self.cleaned_data['psk']
        side_a_device_interface = self.cleaned_data['side_a_device_interface']
        side_a_vm_interface = self.cleaned_data['side_a_vm_interface']
        side_b_device_interface = self.cleaned_data['side_b_device_interface']
        side_b_vm_interface = self.cleaned_data['side_b_vm_interface']

        # Check that interface or vminterface are set
        # if either the Side A or Side B interfaces are assigned
        if side_a_device_interface:
            side_a_assigned_object = side_a_device_interface
            side_a_assigned_object_type = "interface"
            side_a_host_type = "device"
            side_a_host = Interface.objects.get(pk=side_a_assigned_object.pk).device
            side_a_assigned_object_id = Interface.objects.get(pk=side_a_assigned_object.pk).pk
        if side_a_vm_interface:
            side_a_assigned_object = side_a_vm_interface
            side_a_assigned_object_type = "interfaces"
            side_a_host_type = "virtual_machine"
            side_a_host = VMInterface.objects.get(pk=side_a_assigned_object.pk).virtual_machine
            side_a_assigned_object_id = VMInterface.objects.get(pk=side_a_assigned_object.pk).pk
        if side_a_device_interface or side_a_vm_interface:
            side_a_assigned_object_type_id = ContentType.objects.get_for_model(side_a_assigned_object, ).pk
        if side_b_device_interface:
            side_b_assigned_object = side_b_device_interface
            side_b_assigned_object_type = "interface"
            side_b_host_type = "device"
            side_b_host = Interface.objects.get(pk=side_b_assigned_object.pk).device
            side_b_assigned_object_id = Interface.objects.get(pk=side_b_assigned_object.pk).pk
        if side_b_vm_interface:
            side_b_assigned_object = side_b_vm_interface
            side_b_assigned_object_type = "interfaces"
            side_b_host_type = "virtual_machine"
            side_b_host = VMInterface.objects.get(pk=side_b_assigned_object.pk).virtual_machine
            side_b_assigned_object_id = VMInterface.objects.get(pk=side_b_assigned_object.pk).pk
        if side_b_device_interface or side_b_vm_interface:
            side_b_assigned_object_type_id = ContentType.objects.get_for_model(side_b_assigned_object, ).pk

    def save(self, *args, **kwargs):
        # Set assigned object
        self.instance.side_a_assigned_object = (
                self.cleaned_data.get("side_a_device_interface")
                or self.cleaned_data.get("side_a_vm_interface")
        )
        self.instance.side_b_assigned_object = (
                self.cleaned_data.get("side_b_device_interface")
                or self.cleaned_data.get("side_b_vm_interface")
        )
        return super().save(*args, **kwargs)


class TunnelAddForm(TunnelEditForm):
    tunnel_type = ModelChoiceField(
        queryset=TunnelType.objects.all(),
        required=True
    )
    remote_VRF = DynamicModelChoiceField(label='Remote Address VRF', queryset=VRF.objects.all(), required=False)
    b_pub_address = IPNetworkFormField(required=True)

    fields = (
        "name",
        "status",
        "tunnel_type",
        "a_pub_VRF",
        "a_pub_address",
        "b_pub_VRF",
        "b_pub_address",
        "psk",
        "comments",
        "tags",
        "tenant",
    )
    field_order = ["name",
                   "status",
                   "tunnel_type",
                   "a_pub_VRF",
                   "a_pub_address",
                   "b_pub_VRF",
                   "b_pub_address",
                   "psk",
                   "tenant",
                   "comments",
                   "tags"]

    def clean_b_pub_address(self):

        if self.data['remote_VRF'] != '':
            vrf = VRF.objects.get(id=self.data['remote_VRF'])
        else:
            vrf = 0
        try:
            if vrf == 0:
                ip = IPAddress.objects.get(address=str(self.cleaned_data['b_pub_address']))
            else:
                ip = IPAddress.objects.get(address=str(self.cleaned_data['b_pub_address']), vrf=vrf)
        except MultipleObjectsReturned:
            if vrf == 0:
                ip = IPAddress.objects.filter(address=str(self.cleaned_data['b_pub_address'])).first()
            else:
                ip = IPAddress.objects.filter(address=str(self.cleaned_data['b_pub_address']), vrf=vrf).first()
        except ObjectDoesNotExist:
            if vrf == 0:
                ip = IPAddress.objects.create(address=str(self.cleaned_data['b_pub_address']))
            else:
                ip = IPAddress.objects.create(address=str(self.cleaned_data['b_pub_address']), vrf=vrf)
        self.cleaned_data['b_pub_address'] = ip
        return self.cleaned_data['b_pub_address']


class TunnelFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Tunnel instances."""
    model = Tunnel
    status = MultipleChoiceField(choices=TunnelStatusChoices, required=False)
    tenant_id = DynamicModelMultipleChoiceField(
        required=False, queryset=Tenant.objects.all(), label="Tenant"
    )
    tunnel_type = ModelChoiceField(
        queryset=TunnelType.objects.all(),
        required=False
    )
    a_pub_address = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label="Local Address",
    )
    b_pub_address = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label="Remote Address",
    )

    class Meta:
        """Class to define what is used for filtering tunnels with the search box."""
        model = Tunnel
        fields = (
            "a_pub_address",
            "b_pub_address",
            "psk",
            "tunnel_type",
            "tenant_id",
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
