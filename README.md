# 🏠 Personal Dashboard

A customizable personal dashboard integrating **Strava, Spotify, and OpenAI**, with plans for more widgets in the future.

## 🚀 Features

👉 Track fitness activities (**Strava**) 👉 See recently played music (**Spotify**) 👉 AI-powered insights (**OpenAI**)

---

## 🛠 1️⃣ Setup Instructions

### 📅 Clone the Repository

```sh
git clone git@github.com:derekorgan/rinho.git
cd rinho
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
SPOTIFY_REDIRECT_URI="http://localhost:5000/callback"


```

🚨 **DO NOT** commit this file to GitHub! It contains sensitive information. (.env is part of .gitignore)

---

## 🔗 3️⃣ API Authorization Setup

### 🎧 Spotify Authorization

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Register your app and copy the **Client ID & Secret**
3. Add `` as a Redirect URI
4. Run this in your browser:
   ```
   https://accounts.spotify.com/authorize?client_id=your-client-id&response_type=code&redirect_uri=http://localhost:5000/callback&scope=user-read-recently-played
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

Start the Flask server:

```sh
python app.py
```

Then open [**http://127.0.0.1:5000**](http://127.0.0.1:5000) in your browser.

---

## 📀 Next Steps

- 💪 Set up Withings API for weight tracking
- 🌟 Add more widgets (Calendar, Health, Finance, etc.)
- 🤖 Improve AI insights

---

## 📚 License

This project is for **personal use** but can be extended collaboratively.

---

### 🎯 Contributors

- **Derek Organ**


---

