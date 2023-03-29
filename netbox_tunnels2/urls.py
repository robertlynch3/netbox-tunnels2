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
    path("", views.ListTunnelView.as_view(), name="tunnel_list"),
    path("<int:pk>/", views.TunnelView.as_view(), name="tunnel"),
    path("<int:pk>/edit/", views.CreateTunnelView.as_view(), name="tunnel_edit"),
    path("<int:pk>/delete/", views.BulkDeleteTunnelView.as_view(), name="tunnel_delete"),
    path("<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="tunnel_changelog", kwargs={'model': models.Tunnel}),
    path("add/", views.CreateTunnelView.as_view(), name="tunnel_add"),
    path("delete/", views.BulkDeleteTunnelView.as_view(), name="tunnel_bulk_delete")
)