# UDP-Based Traffic Management and Dynamic Prioritization Using SDN

> A Software-Defined Networking (SDN) based traffic management system that generates multiple classes of UDP traffic, detects network congestion, and dynamically prioritizes selected traffic flows to improve Quality of Service (QoS).

---

## 1. Project Overview

Modern computer networks carry different types of traffic simultaneously. However, not all network traffic has the same requirements.

For example:

- **Real-time traffic:** Video calls, voice communication, and online gaming require low latency and minimal jitter.
- **Streaming traffic:** Video and audio streaming require consistent bandwidth and reliable delivery.
- **Background traffic:** File transfers, backups, and bulk data transfers can generally tolerate higher delays.

When multiple traffic flows compete for limited network bandwidth, congestion can occur. This can result in increased latency, packet loss, jitter, and reduced throughput.

Traditional networks generally rely on predefined forwarding and traffic-management configurations. These configurations may not adapt effectively to changing traffic conditions.

This project addresses that problem using **Software-Defined Networking (SDN)**.

We develop a UDP-based traffic generation and monitoring system integrated with an SDN-controlled network. The system identifies different traffic classes, monitors congestion, and dynamically adjusts traffic prioritization to improve network performance.

The project uses **Mininet** to emulate the network, **Open vSwitch (OVS)** as programmable network switches, and an **SDN controller** to manage forwarding and traffic policies.

## 2. Project Objectives

The primary objectives are:

1. Create a virtual network topology consisting of multiple hosts and programmable switches.
2. Generate different classes of UDP traffic simultaneously.
3. Introduce a controlled network bottleneck to simulate congestion.
4. Monitor network performance under different traffic conditions.
5. Use an SDN controller to identify and manage selected traffic flows.
6. Dynamically prioritize important
