# Simple Port Scanner

A small, educational Python port scanner that checks whether TCP ports in a specified range are open on a given IPv4 address or hostname.  
This repository contains `port_scanner.py` — a sequential TCP port scanner built with Python's `socket` and `argparse`, with a little ASCII banner courtesy of `pyfiglet`.

> **Important:** This tool is for learning and authorized testing only. Only scan systems you own or have explicit permission to test.

---

## Table of contents
- [Quick start](#quick-start)  
- [Dependencies](#dependencies)  
- [Command-line arguments (complete)](#command-line-arguments-complete)  
  - `-h`, `--help`  
  - `-t`, `--target`  
  - `-d`, `--DNS`  
  - `-p`, `--ports`  
- [Examples](#examples)  
- [Notes & tips](#notes--tips)  
- [Common errors & fixes](#common-errors--fixes)  
- [Optional enhancements (ideas)](#optional-enhancements-ideas)  
- [Disclaimer & license](#disclaimer--license)

---

## Quick start
1. Put `port_scanner.py` in a folder.  
2. (Optional) Install the ASCII banner dependency:
```bash
pip install pyfiglet
```
3. Run the script (examples below).

---

## Dependencies
- Python 3.7+ (recommended)  
- `pyfiglet` (optional — only used to print the ASCII banner)

Install:
```bash
pip install pyfiglet
```

---

## Command-line arguments (complete)

The script uses Python's `argparse`. Below are the arguments supported, what they accept, defaults, and examples.

### `-h`, `--help`
- **Type:** Flag (no value)  
- **What it does:** Shows the usage message and exits. `argparse` auto-generates this.
- **Usage:**
```bash
python port_scanner.py -h
```
- **Example help excerpt:**
```
usage: port_scanner.py [-h] [-t TARGET] [-d DNS] [-p PORTS]
```

---

### `-t`, `--target`
- **Type:** String — IPv4 address (e.g., `192.168.1.1`)  
- **What it does:** Directly uses the provided IP address as the scan target. The script opens TCP connections to this address on each port in the chosen range.
- **Accepted values:** Valid IPv4 address strings (dotted decimal). The script uses `socket.AF_INET`.
- **Required?** Not strictly; however **either** `--target` **or** `--DNS` must be provided. If both provided, `--DNS` will be resolved and used (current script: if `--DNS` provided, it overrides `--target` resolution path).
- **Example:**
```bash
python port_scanner.py -t 10.0.0.5 -p 20-100
```

---

### `-d`, `--DNS`
- **Type:** String — hostname (e.g., `example.com`)  
- **What it does:** The script resolves the hostname to an IPv4 address using `socket.gethostbyname()` and scans the resolved IP.
- **Accepted values:** Any resolvable domain name. If resolution fails, the script prints an error and stops.
- **Behavior vs `--target`:** Use `--DNS` when you want to supply a domain name. The script resolves the name and then scans the resulting IPv4 address. If you already have a numeric IP, prefer `--target`.
- **Example:**
```bash
python port_scanner.py -d example.com -p 1-1024
```

---

### `-p`, `--ports`
- **Type:** String — port range in format `start-end` (e.g., `1-1024`)  
- **What it does:** Defines the inclusive range of ports to scan. The script splits the argument on `-`, casts both parts to `int`, and iterates `range(start, end+1)`.
- **Accepted format:** `"start-end"` where `start` and `end` are integers between `1` and `65535`.
- **Default:** `1-1024` (if `-p` not provided).
- **Important notes:**
  - Always put the smaller number first: `20-80` not `80-20`. An inverted range may cause unexpected behavior or errors.
  - The script currently performs sequential scanning (one port at a time). Large ranges will be slow.
- **Examples:**
```bash
# default range (1–1024)
python port_scanner.py -t 192.168.1.1

# small range (80 to 90)
python port_scanner.py -d example.com -p 80-90
```

---

## Examples

1. **Scan an IP for default ports (1–1024):**
```bash
python port_scanner.py -t 192.168.1.10
```

2. **Scan a hostname for ports 20–80:**
```bash
python port_scanner.py -d example.com -p 20-80
```

3. **Show the auto-generated help:**
```bash
python port_scanner.py -h
```

---

## Notes & tips
- **Timeout:** The scanner uses `sock.settimeout(1)` inside `scan_port`. If you have slow networks or expect slower responses, increase the timeout in the script (e.g., to `2` or `3` seconds). Decreasing it speeds scanning but risks missing open ports.
- **Performance:** Sequential scans are slow for large ranges. Add threading, `concurrent.futures`, or `asyncio` to speed up scanning.
- **IPv6:** The script uses `AF_INET` (IPv4) only. To support IPv6 you must use `getaddrinfo()` and handle different address families.
- **Output options:** Consider adding a `--output` flag to save results (JSON/CSV/plaintext).
- **Permissions & ethics:** Only scan networks/hosts you own or have explicit permission to test. Unauthorized scanning may be illegal or considered hostile.

---

## Common errors & fixes

- **`socket.gaierror: [Errno -2] Name or service not known`**
  - *Cause:* Hostname couldn't be resolved.
  - *Fix:* Check domain spelling or use `--target` with an IP.

- **`ValueError` when parsing ports**
  - *Cause:* Wrong `-p` format or non-numeric values.
  - *Fix:* Use `-p start-end` with integer values, e.g., `-p 1-1024`.

- **Script is very slow**
  - *Cause:* Large port range + sequential scanning.
  - *Fix:* Implement concurrency or reduce the range.

- **No output for ports you expect to be open**
  - *Cause:* Timeout too short, firewall, or network filtering.
  - *Fix:* Increase `sock.settimeout()` and ensure permission/network access.

---

## Optional enhancements (ideas)
- Add `--timeout <seconds>` to let users set socket timeout from CLI (easy and useful).
- Add `--threads <n>` or `--workers` using `concurrent.futures.ThreadPoolExecutor` for concurrent scanning.
- Add `--output <file>` to save results (CSV/JSON).
- Add UDP scanning mode (requires different logic and caution).
- Add `--verbose` to print closed/filtered port info or debugging details.
- Support IPv6 via `socket.getaddrinfo()` and handling different families.

---

## Disclaimer & license
This tool is for **educational and authorized testing only**. You are responsible for ensuring you have permission to scan any target. The author is **not responsible** for misuse or legal consequences.

This project is intended to be distributed under the MIT License. See the `LICENSE` file for the full text.

---

**One-liner:** *Simple Port Scanner — educational Python TCP port scanner. Use responsibly; scan only with permission.*
