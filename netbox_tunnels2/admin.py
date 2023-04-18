from django.contrib import admin
from .models import Tunnel, TunnelType


@admin.register(Tunnel)
class TunnelAdmin(admin.ModelAdmin):
    """Administrative view for managing Tunnels instances."""

    list_display = ("id", "name", "status", "tunnel_type")


@admin.register(TunnelType)
class TunnelTypeAdmin(admin.ModelAdmin):
    """Administrative view for managing Tunnels to Device instances."""

    list_display = ("id", "name")
