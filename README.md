# Netbox Tunnels Plugin
This plugin is a fork of [jdrew82/netbox-tunnels-plugin](https://github.com/jdrew82/netbox-tunnels-plugin) and [hiddenman/netbox-tunnels-plugin](https://github.com/hiddenman/netbox-tunnels-plugin) in an effort to support Netbox 3.4+. 
<br><br><br>
**In Netbox 3.7, official Tunnel support was added. Please transition to using the build in feature.**
<br><br><br>

## Features
This plugin provide following Models:
* Tunnels
* Tunnel Types

## Compatibility

| NetBox Version | Plugin Version |
|:--------------:|:--------------:|
|   NetBox 3.4   |      0.2.2     |
|   NetBox 3.5   |      0.2.3     |
|   NetBox 3.6   |      0.2.8     |
|   NetBox 3.7 >   |      0.2.9     |


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