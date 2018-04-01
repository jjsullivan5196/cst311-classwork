#!/usr/bin/python
# File: legacy_router.py

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class Router(Node):
    def config(self, **params):
        super(Router, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()

class NetTopo(Topo):
    def build(self, **_opts):
        r1 = self.addNode('r1', cls=Router, ip='10.0.1.1/8')
        s1 = self.addSwitch('s1')

        self.addLink(s1, r1, intfName2='r1-eth1',
                     params2=dict(ip='10.0.1.1/8'))

        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2/8', defaultRoute='via 10.0.1.1')
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1/8', defaultRoute='via 10.0.1.1')

        self.addLink(h1, s1)
        self.addLink(h2, s1)

if __name__ == '__main__':
    setLogLevel('info')
    topo = NetTopo()
    net = Mininet(topo=topo)
    net.start()
    info(net['r1'].cmd('route'))
    CLI(net)
    net.stop()

