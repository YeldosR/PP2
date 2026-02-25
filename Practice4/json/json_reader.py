import json
from pathlib import Path

def load_data(filename):
    base = Path(__file__).parent
    file_path = base / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def print_interfaces(data):
    # Заголовок таблицы
    print("Interface Status")
    print("="*79)
    print(f"{'DN':<50} {'Description':<20} {'Speed':<6} {'MTU':<6}")
    print("-"*50 + " " + "-"*20 + " " + "-"*6 + " " + "-"*6)

    # Проходим по интерфейсам
    for item in data.get("imdata", []):
        attrs = item["l1PhysIf"]["attributes"]
        dn = attrs.get("dn", "")
        desc = attrs.get("descr", "")  # В JSON это обычно 'descr'
        speed = attrs.get("speed", "inherit")
        mtu = attrs.get("mtu", "")
        print(f"{dn:<50} {desc:<20} {speed:<6} {mtu:<6}")

if __name__ == "__main__":
    data = load_data("sample-data.json")
    print_interfaces(data)