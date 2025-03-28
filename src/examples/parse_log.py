from src.utils.time import current_timestamp

def parse_log_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
    print(f"[{current_timestamp()}] Parsed {len(lines)} lines from {path}")