"""
Constants for filters
"""
from django.db.models import Q

TUNNEL_INTERFACE_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="interface")
)