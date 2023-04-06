# Generated by Django 4.1.7 on 2023-04-06 19:30

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import utilities.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0084_staging'),
        ('dcim', '0167_module_status'),
        ('ipam', '0064_clear_search_cache'),
    ]

    operations = [
        migrations.CreateModel(
            name='TunnelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tunnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=64)),
                ('status', models.CharField(default='pending-configuration', max_length=30)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('psk', models.CharField(blank=True, max_length=100)),
                ('comments', models.TextField(blank=True)),
                ('local_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tunnel_local_address', to='ipam.ipaddress')),
                ('local_interface', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dcim.interface')),
                ('remote_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tunnel_remote_address', to='ipam.ipaddress')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('tunnel_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tunnels', to='netbox_tunnels2.tunneltype')),
            ],
            options={
                'verbose_name_plural': 'Tunnels',
            },
        ),
    ]
