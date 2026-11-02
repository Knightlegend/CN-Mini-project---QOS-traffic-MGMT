
import socket
import json
import time
import argparse


def start_client(host, port, traffic_class, flow_id, count, rate, payload_size):

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    payload = b"X" * payload_size

    print(f"Sending {traffic_class} traffic to {host}:{port}")
    print(f"Flow: {flow_id} | Packets: {count} | Rate: {rate} packets/sec\n")

    interval = 1.0 / rate

    for sequence in range(1, count + 1):

        sender_timestamp = time.time_ns()

        metadata = {
            "traffic_class": traffic_class,
            "flow_id": flow_id,
            "sequence_number": sequence,
            "sender_timestamp": sender_timestamp
        }

        header = json.dumps(metadata).encode()

        packet = header + b"\n" + payload

        client.sendto(packet, (host, port))

        print(f"Sent {traffic_class} | Sequence: {sequence}")

        time.sleep(interval)

    print("\nTransmission complete.")
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument(
        "--class-name",
        choices=["HIGH", "MEDIUM", "LOW"],
        required=True
    )
    parser.add_argument("--flow-id", required=True)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--rate", type=float, default=20)
    parser.add_argument("--payload-size", type=int, default=100)

    args = parser.parse_args()

    if args.count <= 0 or args.rate <= 0 or args.payload_size < 0:
        parser.error("Count and rate must be positive; payload size cannot be negative.")

    start_client(
        args.host,
        args.port,
        args.class_name,
        args.flow_id,
        args.count,
        args.rate,
        args.payload_size
    )
