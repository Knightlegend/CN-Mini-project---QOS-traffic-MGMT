# CN-Mini-project : OS-traffic-MGMT

Problem statement:
<img width="1600" height="296" alt="image" src="https://github.com/user-attachments/assets/4474e59c-5719-4df0-be38-9ecb80ee7782" />

# UDP-Based Traffic Generation and SDN-Driven Dynamic Flow Prioritization

## Project Overview

This project implements a UDP-based traffic generation application integrated with Software-Defined Networking (SDN) to dynamically prioritize selected traffic flows during network congestion.

The system generates multiple classes of UDP traffic, simulates network congestion using a bandwidth-constrained bottleneck link, and uses an SDN controller to dynamically modify flow rules and QoS policies to improve network performance.

The project is implemented using Python, Mininet, Open vSwitch (OVS), and an SDN controller.

## Objectives

- Generate multiple classes of UDP traffic with configurable packet sizes and transmission rates.
- Simulate network congestion using a controlled bottleneck link.
- Classify traffic flows based on IP addresses, UDP ports, and traffic characteristics.
- Dynamically prioritize selected traffic using SDN-based QoS mechanisms.
- Monitor network performance through throughput, latency, jitter, and packet loss.
- Compare baseline network performance against the proposed QoS-enabled approach.

## System Architecture

The system consists of three interconnected components:

1. **Network Infrastructure (Data Plane):** A Mininet-based topology with Open vSwitch switches, hosts, and configurable bottleneck links.
2. **Traffic Generation (Application Layer):** UDP client-server applications generating multiple traffic classes and collecting performance measurements.
3. **SDN Controller (Control Plane):** A controller that monitors network conditions, detects congestion, and dynamically modifies flow rules and QoS configurations.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | UDP programming and controller development |
| Mininet | Virtual network topology and traffic simulation |
| Open vSwitch (OVS) | Programmable virtual switching and QoS |
| OpenFlow | Communication between SDN controller and switches |
| Ryu SDN Controller | Network monitoring and dynamic flow management |
| Wireshark | Packet inspection and protocol analysis |
| Matplotlib | Performance visualization and comparison |

## Team Responsibilities

### Person 1 — Network Builder (Data Plane)

**Responsibilities:**
- Design and implement the Mininet network topology.
- Configure hosts, switches, IP addressing, and network links.
- Establish bandwidth-constrained bottleneck links to simulate congestion.
- Configure Open vSwitch queues and QoS mechanisms.
- Ensure connectivity between the network infrastructure and SDN controller.
- Provide a stable, reproducible network environment for integration and testing.

**Deliverable:** Mininet topology implementation with bottleneck and QoS configurations.

### Person 2 — Data Creator (Application Layer)

**Responsibilities:**
- Implement UDP client and server applications using Python sockets.
- Generate multiple traffic classes with configurable packet sizes, rates, and durations.
- Implement packet sequence numbering and timestamp logging.
- Collect throughput, latency, jitter, and packet-loss measurements.
- Generate performance datasets and graphs.
- Compare baseline performance (without QoS) against the proposed SDN-based prioritization approach.

**Deliverable:** UDP traffic generation application with performance logging, evaluation, and comparison.

### Person 3 — Traffic Controller (Control Plane)

**Responsibilities:**
- Implement the SDN controller application using Ryu and OpenFlow.
- Identify and classify traffic flows using IP addresses and UDP ports.
- Monitor switch statistics and detect congestion.
- Integrate congestion notifications from the UDP application, where applicable.
- Dynamically modify flow rules and QoS queue assignments during congestion.
- Restore normal forwarding and QoS policies when congestion subsides.
- Log controller decisions and network state transitions.

**Deliverable:** Dynamic SDN controller capable of congestion-aware traffic prioritization.

## Common Configuration

The following parameters must be agreed upon and maintained consistently across all three components.

| Parameter | Configuration |
|---|---|
| Traffic classes | Real-time, streaming, background |
| UDP ports | 5001, 5002, 5003 |
| Network topology | Agreed Mininet topology |
| Bottleneck bandwidth | Configurable (initial target: 5 Mbps) |
| Bottleneck delay | Configurable (initial target: 10 ms) |
| SDN controller | Ryu |
| OpenFlow version | OpenFlow 1.3 |
| Controller port | 6653 |
| QoS mechanism | Open vSwitch queues and flow rules |
| Congestion detection | Configurable utilization / packet-loss thresholds |
| Results format | CSV with timestamps and packet sequence numbers |

*Note: The above values are initial proposed configurations and may be modified during experimentation.*

## Performance Evaluation

The system is evaluated under two scenarios:

**Scenario 1 — Baseline (Without QoS)**
- All traffic flows use the default forwarding and queueing configuration.
- Congestion is introduced through the bottleneck link.
- Performance metrics are recorded.

**Scenario 2 — Proposed Approach (With SDN QoS)**
- The SDN controller detects congestion.
- Selected traffic flows are dynamically prioritized.
- Performance metrics are recorded under equivalent traffic conditions.

### Evaluation Metrics

- Throughput (Mbps)
- Average latency (ms)
- 95th-percentile latency (ms)
- Jitter (ms)
- Packet loss (%)
- Bottleneck link utilization (%)
- Congestion detection and adaptation time (ms or s)

## Expected Outcome

The proposed system aims to demonstrate that SDN-based dynamic flow prioritization improves the performance of selected traffic classes during network congestion while efficiently utilizing available bandwidth.

The project also evaluates the trade-offs between prioritizing critical traffic and maintaining fairness for lower-priority flows.

## Repository Structure

```text
udp-sdn-prioritizer/
│
├── topology/       # Mininet topology and network configuration
├── traffic/        # UDP client, server and traffic generators
├── controller/     # SDN controller and flow management
├── monitoring/     # Metrics collection and logging
├── experiments/     # Baseline and QoS testing scripts
├── results/        # CSV datasets and performance graphs
├── docs/           # Documentation and architecture
├── requirements.txt
└── README.md
```

## Workflow

1. Establish the Mininet topology and bottleneck link.
2. Start the SDN controller and connect it to the virtual switches.
3. Launch UDP servers and traffic generators.
4. Generate concurrent traffic flows and induce congestion.
5. Monitor traffic and detect congestion.
6. Dynamically apply SDN-based QoS prioritization.
7. Collect performance metrics under both baseline and QoS scenarios.
8. Analyze and compare the results.

## Conclusion

This project demonstrates the integration of UDP socket programming, network emulation, SDN control, and Quality of Service (QoS) mechanisms to build an adaptive traffic management system that responds dynamically to changing network conditions.

