# AutoMSF

This repository contains a Python script for generating a variety of Meterpreter reverse_https payloads for faster use in Offensive Security Experienced Penetration Tester (OSEP) challenges and exams.

## Purpose

The purpose of this script is to automate the process of generating multiple types of reverse_https payloads using msfvenom, a part of the Metasploit framework. The types of payloads generated include C#, EXE, VBS, and PS1. These payloads are copied to the web server's root directory. 

In addition to generating the payloads, the script also automates the process of creating PowerShell commands for downloading and executing each payload. These commands are encoded in base64 for obfuscation. 

Finally, the script starts a multi/handler in Metasploit to listen for incoming connections from the payloads. This allows the script to be a comprehensive solution for generating, deploying, and listening for reverse_https connections in the context of OSEP challenges and exams.

## Usage

This script is designed to be run from the command line with two arguments: LHOST and LPORT. LHOST should be set to the IP address of the host machine (the attacker), and LPORT should be set to the desired listening port on the host machine.

Example usage:

```
python3 AutoMSF.py 192.168.0.1 4444
```

This will generate four types of Meterpreter reverse_https payloads (C#, EXE, VBS, and PS1), each configured to connect back to the IP address 192.168.0.1 on port 4444.

## Prerequisites

To use this script, you will need Python 3 installed on your machine. You will also need the Metasploit framework installed, as the script uses msfvenom to generate payloads and msfconsole to start a multi/handler.

## Warning

Please note that this tool is for educational purposes and authorized testing only. Always obtain proper permission before performing any kind of penetration testing.

## License

This project is licensed under the MIT License. 

## Author

xbz0n

## Disclaimer

This script is intended for lawful, authorized penetration testing activities only. Always obtain proper authorization before conducting penetration testing activities. Misuse of this script could lead to violation of applicable laws. Use responsibly.
