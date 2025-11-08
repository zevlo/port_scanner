# Port Scanner

A multi-threaded TCP port scanner built with Python to detect open ports on target servers. This educational tool demonstrates network programming concepts, multi-threading, and security assessment techniques.

## Overview

Port scanning is the process of sending requests to a range of server ports to determine which ones are open and listening for connections. This tool is designed for:

- **System Administrators**: Verify security policies and audit network services
- **Security Professionals**: Conduct authorized penetration testing and security assessments
- **Students & Developers**: Learn network programming and security concepts

## Key Concepts

- **Port Scanning**: Systematic probing of server ports to identify open services
- **TCP Connection Testing**: Uses TCP handshake attempts to determine port availability
- **Multi-threading**: Concurrent scanning of multiple ports for improved performance
- **Network Security**: Understanding how attackers identify vulnerable services

## Features

- Multi-threaded scanning with 100 concurrent workers
- TCP connection-based port detection
- Hostname and IP address support
- Configurable port ranges
- Clean, readable output
- Pure Python implementation (no external dependencies)

## Requirements

- Python 3.7 or higher
- Standard library only (no external packages required)

## Installation

Clone the repository:

```bash
git clone https://github.com/zevlo/port_scanner.git
cd port_scanner
```

No additional installation required - uses Python standard library only.

## Usage

Basic syntax:

```bash
python port_scanner.py <host> <port-range>
```

### Examples

Scan common ports on localhost:

```bash
python port_scanner.py localhost 20-80
```

Scan web-related ports on a domain:

```bash
python port_scanner.py example.com 80-443
```

Scan a wide range of ports on an IP address:

```bash
python port_scanner.py 192.168.1.1 1-1024
```

### Command-Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `host` | Target hostname or IP address | `localhost`, `192.168.1.1`, `example.com` |
| `ports` | Port range in format "start-end" | `20-80`, `1-65535` |

### Sample Output

```
Opened Port: 22
Opened Port: 80
Opened Port: 443
Scanning completed.
```

## How It Works

### 1. TCP Connection Testing

The scanner uses Python's `socket` library to attempt TCP connections to each port:

```python
def tcp_test(port: int, target_ip: str) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Opened Port: {port}")
```

- Creates a TCP socket (`SOCK_STREAM`)
- Sets 1-second timeout to avoid hanging on unresponsive ports
- Uses `connect_ex()` which returns 0 for successful connections
- Reports open ports immediately upon discovery

### 2. Multi-Threading Architecture

The scanner uses a producer-consumer pattern with threading:

```python
# Create queue and populate with ports
queue = Queue()
for port in range(start_port, end_port + 1):
    queue.put(port)

# Spawn 100 worker threads
for _ in range(100):
    t = threading.Thread(target=worker, args=(target_ip, queue))
    t.daemon = True
    t.start()

# Wait for all tasks to complete
queue.join()
```

**Benefits of Multi-threading:**
- **Concurrent Execution**: 100 ports can be tested simultaneously
- **Performance**: Significantly faster than sequential scanning
- **Thread-Safe Queue**: Prevents race conditions and ensures each port is tested once
- **Daemon Threads**: Automatically terminate when the main program exits

### 3. Workflow

1. **Hostname Resolution**: Converts hostname to IP address using DNS
2. **Queue Population**: Fills thread-safe queue with all ports in range
3. **Worker Dispatch**: Spawns 100 daemon threads to process the queue
4. **Concurrent Testing**: Each thread pulls ports and performs TCP tests
5. **Result Reporting**: Open ports are printed as they're discovered
6. **Completion**: Main thread waits for queue to empty before exiting

## Technical Details

### Socket Programming

- **AF_INET**: IPv4 address family
- **SOCK_STREAM**: TCP socket type
- **connect_ex()**: Non-raising version of connect() - returns error code instead of raising exceptions
- **Timeout**: 1-second timeout prevents indefinite waiting on filtered/unresponsive ports

### Threading Strategy

- **Thread Count**: Fixed pool of 100 threads (adjustable in code)
- **Daemon Threads**: Set to `True` so threads don't prevent program exit
- **Queue Synchronization**: `task_done()` and `join()` ensure all ports are tested before completion

### Performance Characteristics

- **Speed**: Can scan 1000+ ports in seconds (depending on network latency)
- **Scalability**: Efficient for large port ranges (1-65535)
- **Resource Usage**: 100 concurrent threads with minimal memory footprint

## Legal and Ethical Considerations

### Important Disclaimer

Port scanning can be considered an aggressive act and may be illegal without proper authorization. This tool is for **educational purposes only**.

### Guidelines

- **Authorization Required**: Only scan systems you own or have explicit written permission to test
- **Legal Compliance**: Unauthorized port scanning may violate:
  - Computer Fraud and Abuse Act (CFAA) in the United States
  - Computer Misuse Act in the United Kingdom
  - Similar laws in other jurisdictions
- **Responsible Use**: Use this tool ethically for:
  - Personal learning and experimentation on your own systems
  - Authorized security assessments and penetration testing
  - Academic research with proper permissions
  - Professional security audits with signed agreements

### Warning

**The authors and contributors are not responsible for misuse of this tool. Users are solely responsible for ensuring their use complies with applicable laws and regulations.**

## Limitations

- No stealth/evasion techniques (detectable by IDS/IPS)
- TCP-only scanning (no UDP support)
- Basic open/closed detection (no service fingerprinting)
- No output logging or export options
- Fixed timeout and thread count (not configurable via CLI)
- Limited error handling for edge cases

## Future Enhancements

Potential improvements for learning and development:

- [ ] Configurable thread count and timeout via CLI arguments
- [ ] Service banner grabbing and version detection
- [ ] UDP port scanning support
- [ ] Stealth scanning techniques (SYN scan, etc.)
- [ ] Output formats (JSON, CSV, XML)
- [ ] Progress indicator for large scans
- [ ] Port filtering (common ports, specific services)
- [ ] Concurrent host scanning
- [ ] Rate limiting to avoid network flooding
- [ ] Comprehensive error handling and logging
- [ ] Integration with vulnerability databases

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Documentation improvements
- Feature enhancements
- Performance optimizations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Educational Resources

### Learn More About Port Scanning

- [NMAP Documentation](https://nmap.org/book/man.html) - Industry-standard port scanner
- [Python Socket Programming](https://docs.python.org/3/library/socket.html) - Official Python socket documentation
- [Python Threading](https://docs.python.org/3/library/threading.html) - Official Python threading documentation
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) - Security testing methodologies

### Related Concepts

- Network protocols (TCP/IP, UDP)
- Socket programming
- Multi-threading and concurrency
- Network security fundamentals
- Penetration testing methodologies

## Acknowledgments

This project was created for educational purposes to demonstrate:
- Practical application of Python's networking capabilities
- Multi-threaded programming techniques
- Security assessment tool development
- Responsible disclosure and ethical hacking principles

---

**Remember**: With great power comes great responsibility. Use this knowledge to make the internet more secure, not less.
