from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Tunnel, TunnelType

class NestedTunnelSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins:netbox_tunnels2:tunnel')

    class Meta:
        model = Tunnel
        fields = ('id', 'url', 'display', 'name')

class TunnelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins:netbox_tunnels2:tunnel')
    class Meta:
        model = Tunnel
        fields = ('id', 'url', 'display', 'name', 'local_address', 'remote_address', 'status', 'tunnel_type', 'psk', 'tags', 'custom_fields', 'created','last_updated',)
        

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