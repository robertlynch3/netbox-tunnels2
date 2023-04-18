"""
Create views to handle the API logic.
A view set is a single class that can handle the view, add, change,
and delete operations which each require dedicated views under the UI.
"""
from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import TunnelSerializer, TunnelTypeSerializer



class TunnelViewSet(NetBoxModelViewSet):
    queryset = models.Tunnel.objects.all()
    serializer_class = TunnelSerializer
    filterset_class = filtersets.TunnelFilterSet


class TunnelTypeViewSet(NetBoxModelViewSet):
    queryset = models.TunnelType.objects.all()
    serializer_class = TunnelTypeSerializer
    filterset_class = filtersets.TunnelTypeFilterSet