# Netbox Tunnels Plugin
This plugin is a fork of [jdrew82/netbox-tunnels-plugin](https://github.com/jdrew82/netbox-tunnels-plugin) and [hiddenman/netbox-tunnels-plugin](https://github.com/hiddenman/netbox-tunnels-plugin) in an effort to support Netbox 3.4+. 

<!-- Build status with linky to the builds for ease of access.
[![Build Status](https://travis-ci.com/jdrew82/netbox-tunnels-plugin.svg?token=XHesDxGFcPtaq1Q3URi5&branch=master)](https://travis-ci.com/jdrew82/netbox-tunnels-plugin)
 -->
<!-- PyPI version badge.
[![PyPI version](https://badge.fury.io/py/netbox-tunnels-plugin.svg)](https://badge.fury.io/py/netbox-tunnels-plugin)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+NOTE: Please be aware that this plugin is still a work in progress and should not be used for production work at this time!+
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A plugin for [NetBox](https://github.com/netbox-community/netbox) to support documentation of network tunneling
 protocols, ie IPsec, GRE, L2TP, etc.
 -->
 ## Features
This plugin provide following Models:
* Tunnels
* Tunnel Types

## Compatibility

| NetBox Version | Plugin Version |
|:--------------:|:--------------:|
|   NetBox 3.4   |      0.2.2     |
|   NetBox 3.5 >   |      0.2.3     |

This is currently a work in progress.
## Installation
You can install this package from Pip
```
pip install netbox-tunnels2
```

To install the package from source
```
git clone https://github.com/robertlynch3/netbox-tunnels2.git
cd netbox-tunnels2
source /path/to/netbox/venv/bin/activate
python3 setup.py develop
```

Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_tunnels2']
```

Apply the migrations with Netbox `manage.py`:
```
(venv) $ python manage.py migrate
```

Restart Netbox to apply the changes:
```
sudo systemctl restart netbox
```
See [NetBox Documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins) for details

## Screenshots
Tunnel List
![Tunnel List](https://github.com/robertlynch3/netbox-tunnels2/blob/master/docs/img/tunnel-list.png)

Tunnel Details
![Tunnel Details](https://github.com/robertlynch3/netbox-tunnels2/blob/master/docs/img/tunnel-info.png)

## TODO
* Validate the Public IP addresses belong to the Devices
* Validate the same inside interface is not used by multiple tunnels