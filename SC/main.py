import requests
import json
from collections import defaultdict
import os
import random 

# Ganti ini dengan URL raw kamu
RAW_URL = "https://raw.githubusercontent.com/Mayumiwandi/Emilia/refs/heads/main/Data/alive.txt"
OUTPUT_FILENAME = "Alive.json"
OUTPUT_DIR = "Data"

def fetch_and_format(url):
    """
    Fetches proxy data from the URL and groups it by country.
    """
    try:
        response = requests.get(url, timeout=10)
        # This will raise an exception for HTTP error codes (4xx or 5xx)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    data = response.text.strip().splitlines()
    result = defaultdict(list)

    for line in data:
        try:
            # Split the line, expecting at least 3 parts
            parts = line.strip().split(",", 3)
            if len(parts) >= 3:
                ip, port, country = parts[0], parts[1], parts[2]
                # Add the proxy only if the country code is not empty
                if country:
                    result[country].append(f"{ip}:{port}")
        except ValueError:
            # Skip lines that are not formatted correctly
            print(f"Skipping malformed line: {line}")
            continue
            
    return result

def limit_and_randomize_proxies(data, limit=10):
    """
    Limits the number of proxies for each country by taking a random sample.
    """
    if not data:
        return {}
        
    limited_data = {}
    for country, proxies in data.items():
        # 2. Logika diubah di sini
        # Jika jumlah proxy kurang dari atau sama dengan limit, ambil semua.
        if len(proxies) <= limit:
            limited_data[country] = proxies
        # Jika lebih, ambil sampel acak sebanyak limit.
        else:
            limited_data[country] = random.sample(proxies, limit)
    return limited_data

def main():
    """
    Main function to run the script.
    """
    print(f"Fetching data from {RAW_URL}...")
    # 1. Get all the formatted data
    all_formatted_data = fetch_and_format(RAW_URL)

    if all_formatted_data:
        # 2. Limit and randomize the proxies for each country to 10
        print(f"Mengambil {10} proxy acak per negara...")
        limited_data = limit_and_randomize_proxies(all_formatted_data, limit=10)

        # 3. Create directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

        # 4. Save the limited data to the JSON file
        try:
            with open(output_path, "w") as f:
                json.dump(limited_data, f, indent=2)
            print(f"Data berhasil disimpan ke {output_path}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print("Could not process data due to a fetch error.")


if __name__ == "__main__":
    main()
