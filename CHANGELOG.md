# Changelog
## 0.2.9 (2024-01-03)
* Added Netbox 3.7 support
* Renamed the Tunnel model to PluginTunnel to allow for compatibility with Netbox v3.7<br>
Please plan to migrate from `netbox-tunnels2` to the native [Netbox VPN Tunnels model](https://docs.netbox.dev/en/stable/features/vpn-tunnels/)

## 0.2.8 (2023-08-30)
* Added Netbox 3.6 support

## 0.2.7 (2023-08-30)
* Add related tunnels to side A interfaces by @p-rintz in https://github.com/robertlynch3/netbox-tunnels2/pull/14
* Fix permissions for non-admin users by @p-rintz in https://github.com/robertlynch3/netbox-tunnels2/pull/16
* Allow VM assignment to tunnels by @p-rintz in https://github.com/robertlynch3/netbox-tunnels2/pull/18

## 0.2.6 (2023-07-25)
* Add Tenancy support to tunnels by @p-rintz in https://github.com/robertlynch3/netbox-tunnels2/pull/12
* Fix title & align custom fields in template by @p-rintz in https://github.com/robertlynch3/netbox-tunnels2/pull/13


## 0.2.5 (2023-06-23)
* Added the blocks for rendering extra content by registered plugins

## 0.2.4 (2023-05-03)
* Resolved [#4](https://github.com/robertlynch3/netbox-tunnels2/issues/4)

## 0.2.3 (2023-05-03)
* Added Netbox 3.5 support

## 0.2.2 (2023-04-21)
* Resolved [#1](https://github.com/robertlynch3/netbox-tunnels2/issues/1)

## 0.2.1 (2023-04-19)
* Initial release of netbox-tunnels2
* Updated for Netbox v3.4+
* Added tunnel endpoints to denote the inner tunnel interfaces
