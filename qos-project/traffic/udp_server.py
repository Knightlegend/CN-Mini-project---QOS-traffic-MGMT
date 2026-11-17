
import socket
import json
import csv
import time
import argparse
from datetime import datetime


def start_server(host, port, output_file):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))

    print(f"UDP server listening on {host}:{port}")

    received_count = 0
    received_bytes = 0

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
            "packet_size",
            "latency_ms"
        ])

        try:
            while True:
                packet, address = server.recvfrom(65535)

                receiver_time = time.time_ns()

                try:
                    header, payload = packet.split(b"\n", 1)
                    metadata = json.loads(header.decode())

                    sender_time = metadata["sender_timestamp"]
                    latency = (receiver_time - sender_time) / 1_000_000

                    writer.writerow([
                        receiver_time,
                        sender_time,
                        metadata["traffic_class"],
                        metadata["flow_id"],
                        metadata["sequence_number"],
                        address[0],
                        address[1],
                        len(packet),
                        round(latency, 3)
                    ])

                    file.flush()

                    received_count += 1
                    received_bytes += len(packet)

                    print(
                        f"Received {metadata['traffic_class']} | "
                        f"Flow: {metadata['flow_id']} | "
                        f"Sequence: {metadata['sequence_number']}"
                    )

                except (ValueError, KeyError, json.JSONDecodeError):
                    print(f"Invalid packet received from {address}")

        except KeyboardInterrupt:
            print("\nServer stopped.")

        finally:
            print(f"Total packets received: {received_count}")
            print(f"Total data received: {received_bytes} bytes")
            print(f"Results saved to: {output_file}")
            server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument(
        "--output",
        default="results/received_packets.csv"
    )

    args = parser.parse_args()

    start_server(args.host, args.port, args.output)
