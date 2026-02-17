import time
import json
import os
from datetime import datetime

def get_loadavg():
    try:
        with open('/proc/loadavg', 'r') as f:
            data = f.read().strip().split()
            return float(data[0]), float(data[1]), float(data[2])
    except Exception:
        return None, None, None

def get_memfree():
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemFree:'):
                    return int(line.split()[1])
    except Exception:
        return None
    return None

def main():
    load1, load5, load15 = get_loadavg()
    memfree = get_memfree()
    timestamp = int(time.time())
    record = {
        'timestamp': timestamp,
        'load1': load1,
        'load5': load5,
        'load15': load15,
        'memfree_kb': memfree
    }
    now = datetime.now()
    filename = now.strftime('%y-%m-%d-awesome-monitoring.log')
    log_dir = os.path.expanduser('~/logs')
    os.makedirs(log_dir, exist_ok=True)
    filepath = os.path.join(log_dir, filename)
    try:
        with open(filepath, 'a') as f:
            f.write(json.dumps(record) + '\n')
    except Exception as e:
        print(f"Ошибка записи: {e}")

if __name__ == '__main__':
    main()
