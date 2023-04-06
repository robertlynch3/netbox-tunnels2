"""
Creates API endpoint URLs for the plugin.
"""
from netbox.api.routers import NetBoxRouter
from . import views

app_name='netbox_tunnels2'

router = NetBoxRouter()
router.register('tunnels', views.TunnelViewSet)
router.register('tunnel-types', views.TunnelTypeViewSet)

urlpatterns = router.urls