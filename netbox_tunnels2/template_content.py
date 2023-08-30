from extras.plugins import PluginTemplateExtension
from .models import Tunnel
from .tables import RelatedTunnelTable
from django.contrib.contenttypes.models import ContentType


class InterfaceTunnels(PluginTemplateExtension):
    model = 'dcim.interface'

    def full_width_page(self):
        obj = self.context.get('object')
        types = ContentType.objects.get_for_model(obj)
        tunnel = Tunnel.objects.filter(
            side_a_assigned_object_type=types,
            side_a_assigned_object_id=obj.id,
        )
        tunnel_table = RelatedTunnelTable(tunnel)
        return self.render(
            'netbox_tunnels2/interface_extend.html',
            extra_context={
                'related_tunnels': tunnel_table
            }
        )


class VMInterfaceTunnels(PluginTemplateExtension):
    model = 'virtualization.vminterface'

    def full_width_page(self):
        obj = self.context.get('object')
        types = ContentType.objects.get_for_model(obj)
        tunnel = Tunnel.objects.filter(
            side_a_assigned_object_type=types,
            side_a_assigned_object_id=obj.id,
        )
        tunnel_table = RelatedTunnelTable(tunnel)
        return self.render(
            'netbox_tunnels2/interface_extend.html',
            extra_context={
                'related_tunnels': tunnel_table
            }
        )


template_extensions = [InterfaceTunnels, VMInterfaceTunnels]
