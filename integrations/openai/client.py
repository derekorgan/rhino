import openai
from config import OPENAI_CONFIG

class OpenAIClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_CONFIG["api_key"])

    def generate_completion(self, prompt, model="o1-mini"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating completion: {str(e)}"

    def analyze_workout(self, activities, tracks):
        # Move your workout analysis logic here
        prompt = f"""
        I've completed these activities: {activities}
        During these workouts, I listened to these tracks: {tracks}
        Please provide a summary and analysis of my workout sessions.
        """
        return self.generate_completion(prompt)