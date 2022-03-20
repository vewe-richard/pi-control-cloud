# DAY 01

1. reversessh
https://www.howtogeek.com/428413/what-is-reverse-ssh-tunneling-and-how-to-use-it/



2. reverse ssh on pi
2.1 setup remote server
virt-manager generic: ip 192.168.100.168
pi 192.168.1.37

to enable access, need enable host as route:
pi: sudo ip route add 192.168.100.0/24 via 192.168.1.8
host: 
through iptables -L FORWARD --verbose # we see, packet are reject to forward through host
sudo iptables -D FORWARD 11

Next, setup reverssh refer to 1

DAY02
1. reverse ssh test on pi ------- ok
2. setup git repo
3. setup http script
4. script framework --- logger, cmd line parameters, config file

DAY03
1. restruct architecture of the script
