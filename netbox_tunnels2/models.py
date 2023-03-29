"""Tunnel Django model.

(c) 2020 Justin Drew
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel



from utilities.choices import ChoiceSet


class TunnelStatusChoices(ChoiceSet):
    """List of possible status for a Tunnel."""

    STATUS_PENDING_CONFIGURATION = 'pending-configuration'
    STATUS_CONFIGURED = 'configured'
    STATUS_PENDING_DELETION = 'pending-deletion'

    CHOICES = [
        (STATUS_PENDING_CONFIGURATION, 'Pending Configuration', 'orange'),
        (STATUS_CONFIGURED, 'Configured', 'green'),
        (STATUS_PENDING_DELETION, 'Pending Deletion', 'red'),
    ]


class TunnelTypeChoices(ChoiceSet):
    """List of possible types of Tunnels."""

    IPSEC_TUNNEL = "ipsec-tunnel"
    GRE_TUNNEL = "gre-tunnel"
    L2TP_TUNNEL = "l2tp-tunnel"
    PPTP_TUNNEL = "pptp-tunnel"
    CIPE_TUNNEL = "cipe-tunnel"

    CHOICES = (
        (IPSEC_TUNNEL, "IPSec Tunnel"),
        (GRE_TUNNEL, "GRE Tunnel"),
        (L2TP_TUNNEL, "L2TP Tunnel"),
        (PPTP_TUNNEL, "PPTP Tunnel"),
        (CIPE_TUNNEL, "CIPE Tunnel"),
    )



class Tunnel(NetBoxModel):
    """Tunnel model."""
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=30, choices=TunnelStatusChoices, default=TunnelStatusChoices.STATUS_PENDING_CONFIGURATION)
    tunnel_type = models.CharField(max_length=30, choices=TunnelTypeChoices, default=TunnelTypeChoices.IPSEC_TUNNEL)
    src_address = models.CharField(verbose_name="Source Address", max_length=28, blank=True)
    dst_address = models.CharField(verbose_name="Destination Address", max_length=28, blank=True)
    psk = models.CharField(verbose_name="Pre-shared Key", max_length=100, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        """Class to define what will be used to set order based on. Will be using the unique tunnel ID for this purpose."""
        verbose_name_plural='Tunnels'
    def __str__(self):
        """Class to define what identifies the Tunnel object. Will be using name for this."""
        return self.name
    def get_absolute_url(self):
        return reverse('plugins:netbox_tunnels2:tunnel', args=[self.pk])
    def get_status_color(self):
        return TunnelStatusChoices.colors.get(self.status)


# class TunnelDevice(NetBoxModel):
#     """Tunnel to Device relationship."""

#     tunnel = models.ForeignKey(to=Tunnel, on_delete=models.CASCADE, related_name="device")
#     device = models.OneToOneField(to='dcim.Device', on_delete=models.CASCADE, related_name="device_of")

#     class Meta:
#         """Class to define what will be used to set order based on. Will be using the unique tunnel for this purpose."""
