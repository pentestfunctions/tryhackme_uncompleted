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

    # Iterate through pages 1 to 20
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

# Function to fetch progress data for the given room codes
def fetch_progress_data(room_codes, cookie):
    room_codes_str = "%2C".join(room_codes)
    url = f"https://tryhackme.com/api/v2/hacktivities/search-progress?roomCodes={room_codes_str}"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "priority": "u=1, i",
    }
    cookies = {
        "connect.sid": cookie,
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch progress data: {response.status_code}")
        return {}

# Main script execution
rooms = fetch_rooms(cookie)

# Extract room codes
room_codes = [room['code'] for room in rooms]

# Fetch progress data for the rooms
progress_data = fetch_progress_data(room_codes, cookie)

if 'data' in progress_data and 'roomProgress' in progress_data['data']:
    progress_data = progress_data['data']['roomProgress']
else:
    progress_data = []

# Create a dictionary of progress data for quick lookup
progress_dict = {item['roomCode']: item for item in progress_data}

# Add progress data to the rooms
for room in rooms:
    room_code = room['code']
    if room_code in progress_dict:
        room['progress'] = progress_dict[room_code]
    else:
        room['progress'] = {
            'progressPercentage': 0,
            'completedAt': None,
            'lastActivityAt': None
        }

# Save the room list with progress data to a JSON file
with open('all_rooms_with_progress.json', 'w') as f:
    json.dump(rooms, f, indent=4)

print(f"Total rooms fetched: {len(rooms)}")
