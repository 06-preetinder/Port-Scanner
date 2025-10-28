import argparse
import socket
import pyfiglet
import time
import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port}: Open")
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("-t", "--target", type=str, help="Target IP address to scan")
    parser.add_argument("-d", "--DNS", type=str, help="Target hostname to resolve and scan")
    parser.add_argument("-p", "--ports", type=str, default="1-1024", help="Port range to scan (e.g., 1-1024)")
    args = parser.parse_args()

    if not args.target and not args.DNS:
        parser.error("Either --target or --DNS must be provided")

    if args.DNS:
        try:
            target = socket.gethostbyname(args.DNS)
            print(f"Resolved {args.DNS} to {target}")
        except socket.gaierror:
            print(f"Could not resolve hostname: {args.DNS}")
            return
    else:
        target = args.target

    port_range = args.ports.split("-")
    start_port = int(port_range[0])
    end_port = int(port_range[1])
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)
    print("-" * 50)
    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.datetime.now()))
    print("-" * 50)
    for port in range(start_port, end_port + 1):
        scan_port(target, port)

if __name__ == "__main__":
    main()
