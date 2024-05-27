import requests
import json

cookie = "CONNNEC_SID_GOES_HERE"

# Function to fetch rooms from the API
def fetch_rooms(cookie):
    base_url = "https://tryhackme.com/api/v2/hacktivities/extended-search"
    params = {
        "kind": "all",
        "difficulty": "all",
        "order": "relevance",
        "roomType": "all",
        "contentSubType": "free", # Change to 'all' instead for all rooms.
        "limit": 100
    }

    all_rooms = []
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "priority": "u=1, i",
    }
    cookies = {
        "connect.sid": cookie,
    }

    # Iterate through pages 1 to 10
    for page in range(1, 21):
        params["page"] = page
        response = requests.get(base_url, headers=headers, cookies=cookies, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'docs' in data['data']:
                for room in data['data']['docs']:
                    all_rooms.append(room)
        else:
            print(f"Failed to fetch data for page {page}: {response.status_code}")
    
    return all_rooms

# Function to categorize rooms based on the presence of the "Windows" tag
def categorize_rooms(rooms):
    windows_rooms = []
    non_windows_rooms = []

    for room in rooms:
        if any(tag['label'].lower() == 'windows' for tag in room['tagDocs']):
            windows_rooms.append(room)
        else:
            non_windows_rooms.append(room)

    return windows_rooms, non_windows_rooms

# Main script execution
rooms = fetch_rooms(cookie)
windows_rooms, non_windows_rooms = categorize_rooms(rooms)

# Save the categorized room lists to JSON files
with open('windows_rooms.json', 'w') as f:
    json.dump(windows_rooms, f, indent=4)

with open('non_windows_rooms.json', 'w') as f:
    json.dump(non_windows_rooms, f, indent=4)

print(f"Rooms with Windows tag: {len(windows_rooms)}")
print(f"Rooms without Windows tag: {len(non_windows_rooms)}")
