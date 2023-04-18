from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models


class TunnelType(NetBoxObjectType):
    class Meta:
        model=models.Tunnel
        fields = "__all__"
        filterset_class = filtersets.TunnelFilterSet
class TunnelTypeType(NetBoxObjectType):
    class Meta:
        model=models.TunnelType
        fields = "__all__"


class Query(ObjectType):
    tunnel = ObjectField(TunnelType)
    tunnel_list = ObjectListField(TunnelType)

    tunnel_type = ObjectField(TunnelTypeType)
    tunnel_type_list = ObjectListField(TunnelTypeType)


schema = Query