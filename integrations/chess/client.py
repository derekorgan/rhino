import requests
import json
from config import CHESS_CONFIG

class ChessClient:
    def __init__(self):
        self.username = CHESS_CONFIG["username"]
        self.base_url = f"https://api.chess.com/pub/player/{self.username}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def get_profile(self):
        profile_url = self.base_url
        stats_url = f"{self.base_url}/stats"

        profile_response = requests.get(profile_url, headers=self.headers)
        stats_response = requests.get(stats_url, headers=self.headers)

        profile_data = profile_response.json() if profile_response.status_code == 200 else {}
        stats_data = stats_response.json() if stats_response.status_code == 200 else {}

        return profile_data, stats_data

    def get_recent_games(self):
        archives_url = f"{self.base_url}/games/archives"
        response = requests.get(archives_url, headers=self.headers)

        if response.status_code == 200:
            archives = response.json().get("archives", [])
            if archives:
                latest_archive_url = archives[-1]
                games_response = requests.get(latest_archive_url, headers=self.headers)
                return games_response.json().get("games", []) if games_response.status_code == 200 else []
        return []

    def analyze_games(self, openai_client, games):
        if not games:
            return "No recent games available for analysis."

        game_summaries = []
        for game in games[:5]:
            time_control = game.get("time_class", "Unknown").capitalize()
            white_player = game.get("white", {}).get("username", "Unknown")
            black_player = game.get("black", {}).get("username", "Unknown")
            result = game.get("white", {}).get("result", "Unknown")
            game_summaries.append(f"{time_control} | {white_player} vs {black_player} | Result: {result}")

        prompt = f"""
        I have played the following recent chess games:
        {json.dumps(game_summaries, indent=4)}

        Please analyze my performance and suggest areas for improvement.
        """

        try:
            response = openai_client.chat.completions.create(
                model="o1-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating chess insights: {str(e)}"