import socket
import ipaddress

def ipv4_to_6to4_prefix(ipv4_str):
    ipv4 = ipaddress.IPv4Address(ipv4_str)
    hex_ip = hex(int(ipv4))[2:].zfill(8)  # VD: '5639A617'
    group1 = hex_ip[:4]
    group2 = hex_ip[4:]
    return f"2002:{group1}:{group2}::/48"

def resolve_domain_and_convert(domain):
    try:
        ip = socket.gethostbyname(domain)
        prefix = ipv4_to_6to4_prefix(ip)
        print(f"[+] Domain: {domain}")
        print(f"[+] IPv4: {ip}")
        print(f"[+] 6to4 Prefix: {prefix}")
        print(f"[+] Flag: grodno{{{prefix}}}")
    except Exception as e:
        print(f"[!] Error: {e}")

# Ví dụ sử dụng
resolve_domain_and_convert("ctf-spcs.mf.grsu.by")
