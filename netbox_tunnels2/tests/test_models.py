from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from netbox_tunnels2.models import Tunnel, TunnelType
from ipam.models import IPAddress

class TunnelTestCase(TestCase):
    def setUp(self):
        self.tunnelType1 = TunnelType.objects.create(name='GRE', slug='gre')
        self.tunnelType2 = TunnelType.objects.create(name='IPSec Tunnel', slug='ipsec')
        self.ipAddressA = IPAddress.objects.create(address='1.0.0.1/32')
        self.ipAddressB = IPAddress.objects.create(address='1.0.0.2/32')
    def test_tunnel_creation(self):
        tunnel1=Tunnel.objects.create(name='Test Tunnel1', tunnel_type=self.tunnelType1, a_pub_address=self.ipAddressA)
        tunnel1.full_clean()
        self.assertEqual(tunnel1.a_pub_address, self.ipAddressA)


        # Tests an (invalid) Null for a_pub_address
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Tunnel.objects.create(name='Test Tunnel2', tunnel_type=self.tunnelType1, b_pub_address=self.ipAddressA)


        tunnel3=Tunnel.objects.create(name='Test Tunnel3', tunnel_type=self.tunnelType1, a_pub_address=self.ipAddressA, b_pub_address=self.ipAddressB)
        self.assertEqual(tunnel3.a_pub_address, self.ipAddressA)
        self.assertEqual(tunnel3.b_pub_address, self.ipAddressB)
