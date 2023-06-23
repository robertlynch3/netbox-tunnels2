# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

PLUGINS = [
    "netbox_tunnels2",
    "netbox_initializers"    
]

PLUGINS_CONFIG = {  # type: ignore
    "netbox_initializers": {},
    "netbox_tunnels2": {},
}