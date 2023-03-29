from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Tunnel

class NestedTunnelSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_tunnels2-api:tunnels')

    class Meta:
        model = Tunnel
        fields = ('id', 'url', 'display', 'name')

class TunnelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_tunnels2-api:tunnels')
    class Meta:
        model = Tunnel
        fields = ('id', 'display' 'name', 'src_address', 'dst_address', 'status', 'tunnel_type', 'psk', 'tags', 'custom_fields', 'created','last_updated',)