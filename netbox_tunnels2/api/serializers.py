from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ..constants import *
from netbox.api.fields import ContentTypeField

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Tunnel, TunnelType


from netbox.constants import NESTED_SERIALIZER_PREFIX
from utilities.api import get_serializer_for_model
from drf_spectacular.utils import extend_schema_field

class NestedTunnelSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_tunnels2-api:tunnel-detail')

    class Meta:
        model = Tunnel
        fields = (
            'id', 
            'url', 
            'display', 
            'name',
            )

class TunnelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_tunnels2-api:tunnel-detail')
    side_a_assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(TUNNEL_INTERFACE_ASSIGNMENT_MODELS),
        allow_null=True
    )
    side_b_assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(TUNNEL_INTERFACE_ASSIGNMENT_MODELS),
        allow_null=True
    )
    side_a_assigned_object = serializers.SerializerMethodField(read_only=True)
    side_b_assigned_object = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tunnel
        fields = (
            'id', 
            'url', 
            'display', 
            'name', 
            'a_pub_address', 
            'b_pub_address', 
            'side_a_assigned_object_type',
            'side_a_assigned_object_id',
            'side_a_assigned_object',
            'side_b_assigned_object_type',
            'side_b_assigned_object_id',
            'side_b_assigned_object',
            'status', 
            'tunnel_type', 
            'psk', 
            'tags', 
            'custom_fields', 
            'created',
            'last_updated',
        )
    @extend_schema_field(serializers.DictField)
    def get_side_a_assigned_object(self, obj):
        if obj.side_a_assigned_object is None:
            return None
        serializer = get_serializer_for_model(
            obj.side_a_assigned_object,
            prefix=NESTED_SERIALIZER_PREFIX,
        )
        context = {"request": self.context["request"]}
        return serializer(obj.side_a_assigned_object, context=context).data
    def get_side_a_inner_ip(self, obj):
        if obj.side_a_assigned_object is None:
            return None
        serializer = get_serializer_for_model(
            obj.side_a_assigned_object,
            prefix=NESTED_SERIALIZER_PREFIX,
        )
        context = {"request": self.context["request"]}
        return serializer(obj.side_a_assigned_object, context=context).data
    def get_side_b_assigned_object(self, obj):
        if obj.side_b_assigned_object is None:
            return None
        serializer = get_serializer_for_model(
            obj.side_b_assigned_object,
            prefix=NESTED_SERIALIZER_PREFIX,
        )
        context = {"request": self.context["request"]}
        return serializer(obj.side_b_assigned_object, context=context).data
    
    def validate(self, data):
        """
        Validate the Tunnel django model's inputs before allowing it to update the instance.
          - Check that the GFK object is valid.
          - TODO: Check to see if the interface is assigned to another Tunnel
        """
        error_message = {}

        # Check that the GFK object is valid.
        if "side_a_assigned_object_type" in data and "side_a_assigned_object_id" in data:
            # TODO: This can removed after https://github.com/netbox-community/netbox/issues/10221 is fixed.
            try:
                side_a_assigned_object = data[  # noqa: F841
                    "side_a_assigned_object_type"
                ].get_object_for_this_type(
                    id=data["side_a_assigned_object_id"],
                )
            except ObjectDoesNotExist:
                # Sets a standard error message for invalid GFK
                error_message_invalid_gfk = f"Invalid side_a_assigned_object {data['side_a_assigned_object_type']} ID {data['side_a_assigned_object_id']}"
                error_message["side_a_assigned_object_type"] = [error_message_invalid_gfk]
                error_message["side_a_assigned_object_id"] = [error_message_invalid_gfk]
        if "side_b_assigned_object_type" in data and "side_b_assigned_object_id" in data:
            # TODO: This can removed after https://github.com/netbox-community/netbox/issues/10221 is fixed.
            try:
                side_b_assigned_object = data[  # noqa: F841
                    "side_a_assigned_object_type"
                ].get_object_for_this_type(
                    id=data["side_b_assigned_object_id"],
                )
            except ObjectDoesNotExist:
                # Sets a standard error message for invalid GFK
                error_message_invalid_gfk = f"Invalid side_b_assigned_object {data['side_b_assigned_object_type']} ID {data['side_b_assigned_object_id']}"
                error_message["side_b_assigned_object_type"] = [error_message_invalid_gfk]
                error_message["side_b_assigned_object_id"] = [error_message_invalid_gfk]

        if data["side_a_assigned_object_type"].model == "interface":
            interface_host = (
                data["side_a_assigned_object_type"]
                .get_object_for_this_type(id=data["side_a_assigned_object_id"])
                .device
            )
        else:
            a_interface_host = None
        if data["side_b_assigned_object_type"].model == "interface":
            interface_host = (
                data["side_b_assigned_object_type"]
                .get_object_for_this_type(id=data["side_b_assigned_object_id"])
                .device
            )
        else:
            b_interface_host = None

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)

#
# Tunnel Type
#

class NestedTunnelTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins:netbox_tunnels2:tunneltype')

    class Meta:
        model = TunnelType
        fields = ('id', 'url', 'display', 'name')

class TunnelTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins:netbox_tunnels2:tunneltype')

    class Meta:
        model = TunnelType
        fields = ('id', 'url', 'display', 'name',)