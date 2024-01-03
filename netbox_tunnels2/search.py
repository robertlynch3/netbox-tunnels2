from netbox.search import SearchIndex, register_search
from .models import PluginTunnel, TunnelType

@register_search
class TunnelTypeIndex(SearchIndex):
    model=TunnelType
    fields = (
        ('name', 100),
    )
@register_search
class TunnelIndex(SearchIndex):
    model=PluginTunnel
    fields = (
        ('name', 100),
        ('a_pub_address', 150),
        ('b_pub_address', 150),
        ('comments', 5000),
    )