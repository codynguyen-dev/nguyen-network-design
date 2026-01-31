from socket import *
import argparse
from packet import parse_packet

def main():
    parser = argparse.ArgumentParser(description="Phase 1b RDT 1.0 Receiver (UDP)")
    parser.add_argument("--port", type=int, required=True, help="UDP port to bind")
    parser.add_argument("--out", required=True, help="Output file path")
    args = parser.parse_args()

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", args.port))
    print(f"[receiver] listening on UDP port {args.port}")

    expected_seq = 0

    with open(args.out, "wb") as out:
        while True:
            pkt, sender_addr = sock.recvfrom(65535)

            # end signal: 0 len payload packet
            seq, payload = parse_packet(pkt)
            if len(payload) == 0:
                print(f"[receiver] got EOT from {sender_addr}, stopping")
                break

            if seq != expected_seq:
                print(f"[receiver] WARNING: expected seq={expected_seq} but got seq={seq} (dropping)")
                continue

            out.write(payload)
            # print every 50 packets
            if expected_seq % 50 == 0:
                print(f"[receiver] wrote seq={seq} len={len(payload)}")
            expected_seq += 1

    sock.close()
    print("[receiver] done")

if __name__ == "__main__":
    main()