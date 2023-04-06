"""Django urlpatterns declaration for netbox_tunnels plugin.

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
from django.urls import path
from . import views
from netbox.views.generic import ObjectChangeLogView

from . import models

urlpatterns = (
    path("tunnel/", views.ListTunnelView.as_view(), name="tunnel_list"),
    path("tunnel/<int:pk>/", views.TunnelView.as_view(), name="tunnel"),
    path("tunnel/<int:pk>/edit/", views.EditTunnelView.as_view(), name="tunnel_edit"),
    path("tunnel/<int:pk>/delete/", views.DeleteTunnelView.as_view(), name="tunnel_delete"),
    path("tunnel/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="tunnel_changelog", kwargs={'model': models.TunnelType}),
    path("tunnel/add/", views.CreateTunnelView.as_view(), name="tunnel_add"),
    path("tunnel/delete/", views.BulkDeleteTunnelView.as_view(), name="tunnel_bulk_delete"),
    
    path("tunnel-type/", views.ListTunnelTypeView.as_view(), name="tunneltype_list"),
    path("tunnel-type/<int:pk>/", views.TunnelTypeView.as_view(), name="tunneltype"),
    path("tunnel-type/<int:pk>/edit/", views.EditTunnelTypeView.as_view(), name="tunneltype_edit"),
    path("tunnel-type/<int:pk>/delete/", views.DeleteTunnelTypeView.as_view(), name="tunneltype_delete"),
    path("tunnel-type/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="tunneltype_changelog", kwargs={'model': models.TunnelType}),
    path("tunnel-type/add/", views.CreateTunnelTypeView.as_view(), name="tunneltype_add"),
    path("tunnel-type/delete/", views.BulkDeleteTunnelTypeView.as_view(), name="tunneltype_bulk_delete")
)