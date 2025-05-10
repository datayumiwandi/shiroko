import requests
import json
from collections import defaultdict

# Ganti ini dengan URL raw kamu
RAW_URL = "https://raw.githubusercontent.com/Mayumiwandi/Emilia/refs/heads/main/Data/alive.txt"

def fetch_and_format(url):
    response = requests.get(url)
    response.raise_for_status()

    data = response.text.strip().splitlines()
    result = defaultdict(list)

    for line in data:
        ip, port, country, _ = line.strip().split(",", 3)
        result[country].append(f"{ip}:{port}")

    return result

def main():
    formatted_data = fetch_and_format(RAW_URL)
    
    # Simpan ke file JSON
    with open("Data/Alive.json", "w") as f:
        json.dump(formatted_data, f, indent=2)

    print("Data berhasil disimpan ke Data/Alive.json")

if __name__ == "__main__":
    main()
