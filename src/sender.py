from socket import *
import argparse
from packet import make_packet

PAYLOAD_SIZE = 1024

def main():
    parser = argparse.ArgumentParser(description="Phase 1b RDT 1.0 Sender (UDP)")
    parser.add_argument("--host", required=True, help="Receiver host/IP")
    parser.add_argument("--port", type=int, required=True, help="Receiver UDP port")
    parser.add_argument("--file", required=True, help="Input file path")
    args = parser.parse_args()

    sock = socket(AF_INET, SOCK_DGRAM)

    seq = 0
    total_bytes = 0
    with open(args.file, "rb") as f:
        while True:
            chunk = f.read(PAYLOAD_SIZE)
            if not chunk:
                break

            pkt = make_packet(seq, chunk)
            sock.sendto(pkt, (args.host, args.port))

            total_bytes += len(chunk)
            print(f"[sender] sent seq={seq} len={len(chunk)} total={total_bytes}")
            seq += 1

    # send EOT marker: seq = last seq, payload length = 0
    sock.sendto(make_packet(seq, b""), (args.host, args.port))
    print(f"[sender] sent EOT seq={seq}")

    sock.close()
    print("[sender] done")

if __name__ == "__main__":
    main()