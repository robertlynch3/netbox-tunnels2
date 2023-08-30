from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from netbox_tunnels2.models import Tunnel, TunnelType
from dcim.models import Site, DeviceRole, DeviceType, Manufacturer, Device, Interface
from ipam.models import IPAddress
from virtualization.models import VirtualMachine, VMInterface
from tenancy.models.tenants import Tenant


class TunnelTestCase(TestCase):
    def setUp(self):
        self.tunnelType1 = TunnelType.objects.create(name='GRE', slug='gre')
        self.tunnelType2 = TunnelType.objects.create(name='IPSec Tunnel', slug='ipsec')
        self.ipAddressA = IPAddress.objects.create(address='1.0.0.1/32')
        self.ipAddressB = IPAddress.objects.create(address='1.0.0.2/32')
        self.tenant = Tenant.objects.create(name='TestTenant', slug='testtenant')
        site = Site.objects.create(name='test', slug='test')
        manufacturer = Manufacturer.objects.create(name='TestManufacturer', slug='testmanufacturer')
        device_role = DeviceRole.objects.create(name='Firewall', slug='firewall')
        device_type = DeviceType.objects.create(slug='devicetype1', model='DeviceType1', manufacturer=manufacturer)
        self.device = Device.objects.create(
            device_type=device_type, name='device1', device_role=device_role, site=site,
        )
        self.vm = VirtualMachine.objects.create(
            name='test_vm',
            site=site,
        )
        self.interface = Interface.objects.create(name='test_intf', device=self.device, type='virtual')
        self.vminterface = VMInterface.objects.create(name='test_vm_intf', virtual_machine=self.vm)
        self.interface.ip_addresses.add(self.ipAddressA)
        self.vminterface.ip_addresses.add(self.ipAddressB)

    def test_tunnel_creation(self):
        tunnel1 = Tunnel.objects.create(name='Test Tunnel1',
                                        tunnel_type=self.tunnelType1,
                                        a_pub_address=self.ipAddressA,
                                        tenant=self.tenant)
        tunnel1.full_clean()
        self.assertEqual(tunnel1.a_pub_address, self.ipAddressA)
        self.assertEqual(tunnel1.tenant, self.tenant)

        # Tests an (invalid) Null for a_pub_address
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Tunnel.objects.create(name='Test Tunnel2', tunnel_type=self.tunnelType1, b_pub_address=self.ipAddressA)

        tunnel3 = Tunnel.objects.create(name='Test Tunnel3', tunnel_type=self.tunnelType1, a_pub_address=self.ipAddressA, b_pub_address=self.ipAddressB)
        self.assertEqual(tunnel3.a_pub_address, self.ipAddressA)
        self.assertEqual(tunnel3.b_pub_address, self.ipAddressB)

    def test_tunnel_creation_sides(self):
        tunnel = Tunnel.objects.create(name='Test Tunnel1',
                                       tunnel_type=self.tunnelType1,
                                       a_pub_address=self.ipAddressA,
                                       b_pub_address=self.ipAddressB,
                                       side_a_assigned_object_type=ContentType.objects.get_by_natural_key('dcim', 'interface'),
                                       side_a_assigned_object_id=self.interface.id,
                                       side_b_assigned_object_type=ContentType.objects.get_by_natural_key('virtualization', 'vminterface'),
                                       side_b_assigned_object_id=self.vminterface.id,
                                       tenant=self.tenant
                                       )
        tunnel.full_clean(exclude=['side_a_assigned_object_type', 'side_b_assigned_object_type'])
        self.assertEqual(tunnel.a_pub_address, self.ipAddressA)
        self.assertEqual(tunnel.b_pub_address, self.ipAddressB)
        self.assertEqual(tunnel.tenant, self.tenant)
        self.assertEqual(tunnel.side_a_assigned_object, self.interface)
        self.assertEqual(tunnel.side_b_assigned_object, self.vminterface)
