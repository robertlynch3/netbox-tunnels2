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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from netbox.models import NetBoxModel, OrganizationalModel
from utilities.querysets import RestrictedQuerySet
from .constants import TUNNEL_INTERFACE_ASSIGNMENT_MODELS

from dcim.models import Device, Interface




from utilities.choices import ChoiceSet


class TunnelStatusChoices(ChoiceSet):
    CHOICES = [
        ('pending-config', 'Pending Configuration', 'orange'),
        ('configured', 'Configured', 'green'),
        ('pending-deletion', 'Pending Deletion', 'red'),
    ]

class TunnelType(OrganizationalModel):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )
    objects = RestrictedQuerySet.as_manager()


    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_tunnels2:tunneltype', args=[self.pk])


class Tunnel(NetBoxModel):
    """Tunnel model."""
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=30, choices=TunnelStatusChoices, default='pending-config')
    tunnel_type = models.ForeignKey(
        to='TunnelType',
        on_delete=models.PROTECT,
        related_name='tunnels'
    )
    side_a_assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=TUNNEL_INTERFACE_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="side_a_assigned_object_type"
    )
    side_a_assigned_object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )
    side_a_assigned_object = GenericForeignKey(
        ct_field="side_a_assigned_object_type",
        fk_field="side_a_assigned_object_id"
    )
    side_b_assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=TUNNEL_INTERFACE_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="side_b_assigned_object_type"
    )
    side_b_assigned_object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )
    side_b_assigned_object = GenericForeignKey(
        ct_field="side_b_assigned_object_type",
        fk_field="side_b_assigned_object_id"
    )
    a_pub_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='tunnel_a_pub_address',
        verbose_name="Side A Public Address"
    )
    b_pub_address=models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='tunnel_b_pub_address',
        verbose_name="Side B Public Address",
        null=True,
        blank=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
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


GenericRelation(
    to=Tunnel,
    content_type_field="side_a_assigned_object_type",
    object_id_field="side_a_assigned_object_id",
    related_query_name="interface",
).contribute_to_class(Interface, "tunnelassignments")
GenericRelation(
    to=Tunnel,
    content_type_field="side_a_assigned_object_type",
    object_id_field="side_a_assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "tunnels")
GenericRelation(
    to=Tunnel,
    content_type_field="side_b_assigned_object_type",
    object_id_field="side_b_assigned_object_id",
    related_query_name="interface",
).contribute_to_class(Interface, "tunnelassignments_b")
GenericRelation(
    to=Tunnel,
    content_type_field="side_b_assigned_object_type",
    object_id_field="side_b_assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "tunnels_b")