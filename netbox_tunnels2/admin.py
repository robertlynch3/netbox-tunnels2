from django.contrib import admin
from .models import PluginTunnel, TunnelType


@admin.register(PluginTunnel)
class TunnelAdmin(admin.ModelAdmin):
    """Administrative view for managing Tunnels instances."""

    list_display = ("id", "name", "status", "tunnel_type")


@admin.register(TunnelType)
class TunnelTypeAdmin(admin.ModelAdmin):
    """Administrative view for managing Tunnels to Device instances."""

    list_display = ("id", "name")
