# Collector Tool

**Version:** 3.1.0

A versatile, all-in-one network and web reconnaissance toolkit designed for both security professionals and developers. `collector.py` consolidates HTTP method fuzzing, link extraction, DNS and WHOIS lookups, social network enumeration (SNSE), subdomain discovery, and a suite of port-scanning techniques into a single, streamlined command-line interface.

---

## Key Features

* **HTTP Fuzzing & Link Extraction**: Test supported HTTP methods or fuzz custom ones; extract and save all discovered links from a target.
* **DNS Lookup & Zone Transfers**: Perform standard record queries (A, AAAA, MX, NS, SOA, TXT) or attempt zone transfers when allowed.
* **WHOIS Queries**: Retrieve registration details for domains, IPs, or networks through a unified interface.
* **Social Network Search (SNSE)**: Enumerate user profiles across platforms like Google or Bing via the SNSE module.
* **Subdomain Scanning**: Brute-force discover subdomains using custom wordlists with adjustable threading and verbosity.
* **Port Scanners**:
  * **TCP & ACK**: Detect open and filtered ports with root-level ACK scans.
  * **SYN (Stealth)**, **FIN**, **NULL**, **XMAS**, **UDP**: Employ a variety of TCP and UDP scanning techniques for comprehensive coverage.

---

## Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/your-org/collector-tool.git
   cd collector-tool
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure root privileges** (required for certain scans):

   ```bash
   sudo ./collector.py --help
   ```

---

## Usage

Run `collector.py` with the desired subcommand and options. At minimum, specify a target domain/IP via `-d/--domain`.

```bash
# HTTP fuzzing (all methods)
./collector.py -d example.com crawl --method ALL

# Extract links only
./collector.py -d example.com crawl --extract --outfile links.txt

# Standard TCP scan (default)
./collector.py -d 192.168.1.10 scan -p default --timeout 0.5

# Root-required ACK scan
sudo ./collector.py -d 192.168.1.10 scan -p 1-1024 --tech ack

# Subdomain brute-force with custom wordlist
./collector.py -d example.com subscan --wordlist common-subdomains.txt

# DNS lookup for MX and TXT records
./collector.py -d example.com dns -t MX -t TXT

# WHOIS lookup for domain and network
./collector.py -d example.com whois --dom --net

# Social network enumeration on Bing
./collector.py -d target.com snse --engine bing
```

---

## Configuration & Customization

* **User Agents**: Modify `USER_AGENTS` in the script to add or rotate through different headers.
* **Threading**: Adjust `--threads` to control concurrency for scans and enumeration.
* **Timeouts**: Fine-tune `--timeout` for responsiveness versus thoroughness.

---

## Contributing

Please submit issues or pull requests via GitHub. Adhere to the existing 2-space indentation, add unit tests for new modules, and update this README with any new features or flags.

---

## License

GPL License. See [LICENSE](LICENSE) for details.
