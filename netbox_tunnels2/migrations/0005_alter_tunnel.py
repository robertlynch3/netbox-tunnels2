# Generated by Django 4.2.8 on 2024-01-03 18:42

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import utilities.json


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0069_gfk_indexes"),
        ("tenancy", "0013_gfk_indexes"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0105_customfield_min_max_values"),
        ("netbox_tunnels2", "0004_alter_tunnel_side_a_assigned_object_type_and_more"),
    ]

    operations = [
        migrations.RenameModel('Tunnel','PluginTunnel')
    ]
