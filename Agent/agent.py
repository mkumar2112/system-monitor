import psutil
import platform
import socket
import requests

API_URL = "http://127.0.0.1:8000/api/upload_system_data/"

def collect_system_info():
    cpu_freq = psutil.cpu_freq()
    disk = psutil.disk_usage('/')

    return {
        "name": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os_name": platform.system(),
        "os_version": platform.version(),
        "processor_name": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "max_frequency_mhz": round(cpu_freq.max,2) if cpu_freq else None,
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "total_storage_gb": round(disk.total / (1024**3),2),
        "used_storage_gb": round(disk.used / (1024**3),2),
        "free_storage_gb": round(disk.free / (1024**3),2)
    }

def collect_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'memory_info', 'ppid']):
        try:
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "user": proc.info['username'],
                "status": proc.info['status'],
                "memory": proc.info['memory_info'].rss / (1024*1024),
                "parent": proc.info['ppid']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

if __name__ == "__main__":
    data = {
        "computer": collect_system_info(),
        "processes": collect_processes()
    }

    resp = requests.post(API_URL, json=data)
    print(resp.status_code, resp.text)
