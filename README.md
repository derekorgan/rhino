# 🦏 Rhino Workout & Music Tracker 
### (Playground experiment app) 

A FastAPI web application that integrates with Strava, Spotify, and OpenAI to track workouts, music, and provide AI-powered insights.

<p align="center">
  <img src="https://raw.githubusercontent.com/derekorgan/rhino/main/app/static/images/rhino_app_icon.jpg" width="150" alt="Rhino Dashboard Logo">
</p>


## 🚀 Features

👉 Track fitness activities (**Strava**) 👉 See recently played music (**Spotify**) 👉 AI-powered insights (**OpenAI**)

---

## 🛠 1️⃣ Setup Instructions

### 📅 Clone the Repository

```sh
git clone git@github.com:derekorgan/rhino.git
cd rhino
```

### 📦 Install Dependencies

Make sure you have Python installed. Then run:

```sh
pip install -r requirements.txt
```

---

## 🔑 2️⃣ Setting Up Your `.env` File

### 📌 Step 1: Create `.env` File

Inside the project root, create a `.env` file:

```sh
touch .env
```

### 📌 Step 2: Add Your API Keys

Open `.env` and add the following:

```ini
# OpenAI API Key
OPENAI_API_KEY="your-openai-api-key"

# Strava API Credentials
STRAVA_CLIENT_ID="your-strava-client-id"
STRAVA_CLIENT_SECRET="your-strava-client-secret"
STRAVA_REFRESH_TOKEN="your-strava-refresh-token"

# Spotify API Credentials
SPOTIFY_CLIENT_ID="your-spotify-client-id"
SPOTIFY_CLIENT_SECRET="your-spotify-client-secret"
SPOTIFY_REDIRECT_URI="http://localhost:8000/callback"

# Chess.com API username (optional)
CHESS_USERNAME = "your-username"

# Withings settings (optional)
WITHINGS_CLIENT_ID="your-withings-client-id"
WITHINGS_CLIENT_SECRET="your-withings-client-secret"
WITHINGS_REDIRECT_URI="your-withings-redirect-uri"
WITHINGS_REFRESH_TOKEN="your-withings-refresh-token"
```

🚨 **DO NOT** commit this file to GitHub! It contains sensitive information. (.env is part of .gitignore)

---

## 🔗 3️⃣ API Authorization Setup

### 🎧 Spotify Authorization

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Register your app and copy the **Client ID & Secret**
3. Add `http://localhost:8000/callback` as a Redirect URI
4. Run this in your browser:
   ```
   https://accounts.spotify.com/authorize?client_id=your-client-id&response_type=code&redirect_uri=http://localhost:8000/callback&scope=user-read-recently-played
   ```
5. Copy the **code** from the URL and exchange it for an access token.

---

### 🏃 Strava Authorization

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Copy **Client ID, Secret, and Refresh Token**
3. Exchange the refresh token for an access token:
   ```sh
   curl -X POST https://www.strava.com/oauth/token \
   -d client_id=your-client-id \
   -d client_secret=your-client-secret \
   -d grant_type=refresh_token \
   -d refresh_token=your-refresh-token
   ```
4. Add the tokens to your `.env` file.

---

### 🤖 OpenAI Authorization

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Generate a new API key
3. Add it to your `.env` file.

---

## 🛠 4️⃣ Running the App

Start the FastAPI server:

```sh
uvicorn app.main:app --reload
# or
python -m app.main
```

Then open [**http://127.0.0.1:8000**](http://127.0.0.1:8000) in your browser.

---

## 📀 Next Steps

- 💪 Set up Withings API / Dartcounter for weight tracking and darts
- 🌟 Add more widgets (Calendar, Health, Finance, etc.)
- 🤖 Improve AI insights

---

## 📚 License

This project is for **personal use** but can be extended collaboratively.

---

### 🎯 Contributors

- **Derek Organ**

## Prerequisites

- Python 3.8 or higher
- Strava API credentials
- Spotify Developer account and API credentials
- Chess.com account (optional)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rhino.git
cd rhino
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development

### Project Organization
- The application follows a modern FastAPI structure:
  - `app/` - Main application package
  - `app/main.py` - Entry point with FastAPI app initialization
  - `app/api/` - API routes and endpoints
  - `app/core/` - Core functionality, configs, and dependencies
  - `app/models/` - Pydantic models and schemas
  - `app/services/` - Service integrations (Strava, Spotify, OpenAI)
  - `app/static/` - Static assets (CSS, images)
  - `app/templates/` - Jinja2 templates for rendering

### Adding New Features
1. Define Pydantic models in `app/models/`
2. Implement service logic in `app/services/`
3. Create API routes in `app/api/routes/`
4. Add dependencies to `app/core/dependencies.py` if needed

## Dependencies

- FastAPI: Modern web framework with automatic OpenAPI docs
- Pydantic: Data validation and settings management
- Uvicorn: ASGI server for FastAPI
- Jinja2: Templating engine
- Python-dotenv: Environment variable management
- Additional requirements in `requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

Common issues and solutions:
- API rate limiting: Implement proper caching
- Authentication errors: Check `.env` file and API credentials
- Module import errors: Ensure correct virtual environment activation

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Strava API Documentation](https://developers.strava.com/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Chess.com API](https://www.chess.com/news/view/published-data-api)
- [OpenAI API](https://platform.openai.com/docs/api-reference)

---