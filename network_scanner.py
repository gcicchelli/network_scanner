import platform
import subprocess
import threading
import socket
from datetime import datetime

port_names = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    8080: "Alt HTTP / Web Interface",
    5000: "Flask / Dev Web",
    6379: "Redis",
    8000: "Dev Web / HTTP Alt",
    8443: "HTTPS Alt",
    9000: "Dev / Custom",
    10000: "Webmin / Admin Panel"
}

def log_result(ip, open_ports_named, filename="scan_log.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {ip} - Open ports: {open_ports_named}\n"
    with open(filename, "a") as f:
        f.write(entry)

def ping_and_scan(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        subprocess.check_output(command, stderr=subprocess.DEVNULL)
        open_ports = scan_ports(ip)
        if open_ports:
            open_ports_named = [(p, port_names.get(p, "Unknown")) for p in open_ports]
            print(f"✅ {ip} - Open ports: {open_ports_named}")
            log_result(ip, open_ports_named)
        else:
            print(f"✅ {ip} - No common ports open")
    except subprocess.CalledProcessError:
        pass

def scan_ports(ip, ports=[21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 8080, 5000, 6379, 8000, 8443, 9000, 10000]):
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)  # fast scan
        try:
            s.connect((ip, port))
            open_ports.append(port)
        except:
            pass  # port is closed or unreachable
        finally:
            s.close()
    return open_ports

def scan_subnet(base_ip):
    threads = []
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        thread = threading.Thread(target=ping_and_scan, args=(ip,))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()

if __name__ == "__main__":
    scan_subnet("your_ip_address_here") 
