from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo ( Topo ):


  def __init__( self ):

	Topo.__init__( self )

	host1 = self.addHost( 'h1' )
	host2 = self.addHost( 'h2' )
	host3 = self.addHost( 'h3' )
	host4 = self.addHost( 'h4' )
	host5 = self.addHost( 'h5' )
	host6 = self.addHost( 'h6' )
	switch1 = self.addSwitch( 'sw1' )
	switch2 = self.addSwitch( 'sw2' )
	switch3 = self.addSwitch( 'sw3' )
	switch4 = self.addSwitch( 'sw4' )
	#switch5 = self.addSwitch( 'sw5' )
	#switch6 = self.addSwitch( 'sw6' )

	self.addLink( host1,switch1 )
	self.addLink( host2,switch1 )
	self.addLink( host3,switch2 )
	self.addLink( host4,switch3 )
	self.addLink( host5,switch3 )
	self.addLink( host6,switch4 )
	#self.addLink( switch1,switch4 )
	self.addLink( switch1,switch3, bw = 100 )
	self.addLink( switch2,switch3, bw = 20 )
	self.addLink( switch2,switch4, bw = 80 )
	#self.addLink( switch5,switch3, bw = 3 )
	#self.addLink( switch5,switch2, bw = 1 )
	#self.addLink( switch6,switch1, bw = 3 )
	self.addLink( switch1,switch4, bw = 50 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
