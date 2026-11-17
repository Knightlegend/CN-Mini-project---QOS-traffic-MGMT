import socket
import threading
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet,ipv4,udp

class controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    port_to_queue={5001:1,5002:2,5003:3}    
    def __init__(self, *args, **kwargs):
        super(controller, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.qos_targets = set()
        self.notified=set()
        threading.Thread(target=self.socket_listener, daemon=True).start()

    def socket_listener(self):
        localIP="0.0.0.0"
        localPort=20001
        bufferSize=1024

        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((localIP, localPort))

        print("UDP server up and listening")

        while(True):
            message,address= UDPServerSocket.recvfrom(bufferSize)
            try:
                target_ip, port = message.decode('utf-8').strip().split(",")
                port = int(port)
            except ValueError:
                print("Invalid notification format")
                continue
            
            if port not in self.port_to_queue:
                print(f"Unkown port: {port}")
                continue
                
            self.notified.add((target_ip,port))
            print(f"Notification received: {target_ip}, port {port}")
            print(f"Client address: {address}")

            UDPServerSocket.sendto(b"Notification received", address)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        self.datapaths[datapath.id] = datapath
        print(f"Switch connected: DPID {datapath.id}")

        flags = ofproto.OFPC_FRAG_NORMAL 
        miss_send_len = 256
        

        config_req = parser.OFPSetConfig(datapath, flags, miss_send_len)
        datapath.send_msg(config_req)
        print(f"Pushed Switch Configuration (miss_send_len={miss_send_len})")
        
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=0, match=match, instructions=inst)
        datapath.send_msg(mod)

 
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]

        if msg.data and datapath.id == 1:
            pack = packet.Packet(msg.data)
            ip_header = pack.get_protocol(ipv4.ipv4)
            udp_header = pack.get_protocol(udp.udp)

            if ip_header and udp_header:
                target_ip = ip_header.dst
                port = udp_header.dst_port
                queue = self.port_to_queue.get(port)

                if target_ip == "10.0.0.3" and queue is not None:
                    key = (target_ip, port)

                    if key in self.notified:
                        actions = [parser.OFPActionSetQueue(queue),parser.OFPActionOutput(3)]

                        if key not in self.qos_targets:
                            match = parser.OFPMatch(eth_type=0x0800,ip_proto=17,ipv4_dst=target_ip,udp_dst=port)
                            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,[parser.OFPActionSetQueue(queue),parser.OFPActionOutput(3)])]

                            mod = parser.OFPFlowMod(datapath=datapath,priority=200,match=match,instructions=inst)

                            datapath.send_msg(mod)
                            self.qos_targets.add(key)

                            print(f"QoS installed, Port: {port}, Queue: {queue}")

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)
