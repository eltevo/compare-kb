Configure NAT in Windows 10 for Hyper-V
(This will not enable DHCP but will do network forwarding)

    PS> New-VMSwitch –SwitchName “NATSwitch” –SwitchType Internal
    PS> New-NetIPAddress –IPAddress 192.168.137.1 -PrefixLength 24 -InterfaceAlias "vEthernet (NATSwitch)"
    PS> New-NetNat –Name NATnetwork –InternalIPInterfaceAddressPrefix 192.168.137.0/24
