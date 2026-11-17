
import socket
import json
import csv
import time
import argparse
import selectors
import os
import math


TRAFFIC_PORTS = {
    "HIGH": 5001,
    "MEDIUM": 5002,
    "LOW": 5003
}


def percentile(values, percent):

    if not values:
        return 0

    sorted_values = sorted(values)

    index = math.ceil((percent / 100) * len(sorted_values)) - 1

    return sorted_values[max(0, index)]


def start_server(host, output_file):

    selector = selectors.DefaultSelector()
    sockets = []

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    for traffic_class, port in TRAFFIC_PORTS.items():

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((host, port))

        selector.register(server, selectors.EVENT_READ, traffic_class)
        sockets.append(server)

        print(f"Listening for {traffic_class} traffic on {host}:{port}")

    print("\nUDP QoS server running.")
    print("Press Ctrl+C to stop.\n")

    received_count = 0
    received_bytes = 0

    flow_stats = {}

    with open(output_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "receiver_timestamp",
            "sender_timestamp",
            "traffic_class",
            "flow_id",
            "sequence_number",
            "source_ip",
            "source_port",
            "destination_port",
            "packet_size",
            "latency_ms"
        ])

        try:

            while True:

                events = selector.select(timeout=1)

                for key, mask in events:

                    server = key.fileobj
                    port_class = key.data

                    packet, address = server.recvfrom(65535)

                    receiver_time = time.time_ns()
                    receive_monotonic = time.monotonic()

                    try:

                        header, payload = packet.split(b"\n", 1)
                        metadata = json.loads(header.decode())

                        traffic_class = metadata["traffic_class"]
                        flow_id = metadata["flow_id"]
                        sequence = metadata["sequence_number"]
                        sender_time = metadata["sender_timestamp"]
                        expected = metadata["expected_packets"]

                        if traffic_class != port_class:
                            print("Traffic class and destination port mismatch.")
                            continue

                        latency = (receiver_time - sender_time) / 1_000_000

                        flow_key = (
                            address[0],
                            address[1],
                            flow_id,
                            traffic_class
                        )

                        if flow_key not in flow_stats:

                            flow_stats[flow_key] = {
                                "expected": expected,
                                "sequences": set(),
                                "received": 0,
                                "bytes": 0,
                                "latencies": [],
                                "first_time": receive_monotonic,
                                "last_time": receive_monotonic
                            }

                        stats = flow_stats[flow_key]

                        stats["expected"] = max(stats["expected"], expected)
                        stats["received"] += 1
                        stats["sequences"].add(sequence)
                        stats["bytes"] += len(packet)
                        stats["latencies"].append(latency)
                        stats["last_time"] = receive_monotonic

                        writer.writerow([
                            receiver_time,
                            sender_time,
                            traffic_class,
                            flow_id,
                            sequence,
                            address[0],
                            address[1],
                            server.getsockname()[1],
                            len(packet),
                            round(latency, 3)
                        ])

                        file.flush()

                        received_count += 1
                        received_bytes += len(packet)

                        print(
                            f"Received {traffic_class} | "
                            f"Flow: {flow_id} | "
                            f"Sequence: {sequence}"
                        )

                    except (
                        ValueError,
                        KeyError,
                        TypeError,
                        json.JSONDecodeError
                    ):

                        print(f"Invalid packet received from {address}")

        except KeyboardInterrupt:

            print("\nServer stopped.")

        finally:

            print("\n========== SERVER SUMMARY ==========")

            print(f"Total packets received: {received_count}")
            print(f"Total data received: {received_bytes} bytes")

            print("\n========== PER-FLOW QoS SUMMARY ==========")

            for flow_key, stats in flow_stats.items():

                source_ip, source_port, flow_id, traffic_class = flow_key

                unique_received = len(stats["sequences"])

                expected = stats["expected"]

                lost = max(0, expected - unique_received)

                loss_percentage = (
                    (lost / expected) * 100 if expected > 0 else 0
                )

                latencies = stats["latencies"]

                avg_latency = (
                    sum(latencies) / len(latencies) if latencies else 0
                )

                min_latency = min(latencies) if latencies else 0
                max_latency = max(latencies) if latencies else 0

                p95_latency = percentile(latencies, 95)

                elapsed = stats["last_time"] - stats["first_time"]

                throughput = (
                    (stats["bytes"] * 8) / elapsed / 1_000_000
                    if elapsed > 0 else 0
                )

                print(f"\nTraffic class: {traffic_class}")
                print(f"Flow ID: {flow_id}")
                print(f"Source: {source_ip}:{source_port}")

                print(f"Expected packets: {expected}")
                print(f"Received datagrams: {stats['received']}")
                print(f"Unique packets received: {unique_received}")
                print(f"Lost packets: {lost}")
                print(f"Packet loss: {loss_percentage:.2f}%")

                print(f"Average latency: {avg_latency:.3f} ms")
                print(f"Minimum latency: {min_latency:.3f} ms")
                print(f"Maximum latency: {max_latency:.3f} ms")
                print(f"P95 latency: {p95_latency:.3f} ms")

                print(f"Throughput: {throughput:.3f} Mbps")

            print("\n====================================")
            print(f"Results saved to: {output_file}")

            selector.close()

            for server in sockets:
                server.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="QoS UDP traffic receiver and measurement server"
    )

    parser.add_argument("--host", default="0.0.0.0")

    parser.add_argument(
        "--output",
        default="results/received_packets.csv"
    )

    args = parser.parse_args()

    start_server(args.host, args.output)
