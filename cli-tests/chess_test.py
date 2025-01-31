import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def pretty_print(data):
    print(json.dumps(data, indent=4))

CHESS_USERNAME = os.getenv("CHESS_USERNAME")  # Replace with a different username if needed

BASE_URL = "https://api.chess.com/pub/player"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_player_profile(username):
    url = f"{BASE_URL}/{username}"
    response = requests.get(url, headers=HEADERS)  # Added headers
    print(f"Fetching profile from: {url}")  
    print(f"Response: {response.status_code} - {response.text}")  
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to fetch profile. Status Code: {response.status_code}"}


# Fetch rating stats
def get_player_stats(username):
    url = f"{BASE_URL}/{username}/stats"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to fetch stats. Status Code: {response.status_code}"}


if __name__ == "__main__":
    print("🔹 Chess.com Profile Data:")
    profile = get_player_profile(CHESS_USERNAME)
    pretty_print(profile)
    
    print("\n🔹 Player Rating Stats:")
    pretty_print(get_player_stats(CHESS_USERNAME))
    
