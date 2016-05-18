Configure IPTABLES
---------------------------------

Install persist package

# apt-get install iptables-persistent

https://help.ubuntu.com/community/IptablesHowTo

Should look like this:

target     prot opt source               destination
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:http
ACCEPT     tcp  --  157.181.0.0/16       anywhere             tcp dpt:ssh
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
REJECT     tcp  --  anywhere             anywhere             reject-with icmp-port-unreachable
REJECT     udp  --  anywhere             anywhere             reject-with icmp-port-unreachable

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination

# iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT
# iptables -I INPUT 2 -p tcp -s 157.181.0.0/16 --dport 22 -j ACCEPT
# iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
# iptables -A INPUT -p tcp -j REJECT
# iptables -A INPUT -p udp -j REJECT

Rules to access Dell OpenManage from local networks (complex, itl)

# iptables -I INPUT 8 -p tcp --dport 1311 -s "157.181.168.0/24" -j ACCEPT
# iptables -I INPUT 8 -p tcp --dport 1311 -s "157.181.172.64/26" -j ACCEPT


Save settings so they will be applied at next boot.

# service iptables-persistent save