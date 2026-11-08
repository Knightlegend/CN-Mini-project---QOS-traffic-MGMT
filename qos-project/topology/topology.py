
#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def build_network():
    net = Mininet(
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True,
        build=False
    )

    info("*** Creating hosts\n")
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")
    h3 = net.addHost("h3", ip="10.0.0.3/24")

    info("*** Creating standalone switches\n")
    s1 = net.addSwitch(
        "s1",
        protocols="OpenFlow13",
        failMode="standalone"
    )
    s2 = net.addSwitch(
        "s2",
        protocols="OpenFlow13",
        failMode="standalone"
    )

    info("*** Connecting h1 and h2 to s1\n")
    net.addLink(h1, s1, bw=20)
    net.addLink(h2, s1, bw=20)

    info("*** Connecting h3 to s2\n")
    net.addLink(h3, s2, bw=20)


    info("*** Creating 5 Mbps bottleneck\n")
    net.addLink(
        s1,
        s2,
        bw=20,
        delay="10ms",
        max_queue_size=50
    )

    info("*** Starting network\n")
    net.build()
    net.start()

    info("*** Network topology is running\n")
    info("*** Type 'pingall' to test connectivity\n")
    info("*** Type 'exit' to stop the network\n")

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    build_network()
