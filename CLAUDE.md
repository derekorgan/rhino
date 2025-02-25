# CLAUDE.md: Rhino - Personal Dynamic AI Dashboard

## Project Overview
This is a FastAPI experiment project to build a Personal Dynamic AI Dashboard that integrates various data sources and provides AI-powered insights. The dashboard connects to services like Strava, Spotify, OpenAI, and others to create a comprehensive personal data hub.

## Application Commands
- Run the app: `source env/bin/activate && python -m app.main` or `uvicorn app.main:app --reload`
- CLI tests:
  - Strava: `python cli-tests/strava_test.py`
  - Spotify: `python cli-tests/spotify_test.py` 
  - OpenAI: `python cli-tests/openai_test.py`
  - Chess: `python cli-tests/chess_test.py`

## Code Style Guidelines
- **Imports**: Standard lib → Third-party packages → Local modules
- **Naming**: 
  - Classes: PascalCase (StravaClient)
  - Functions/variables: snake_case (get_activities)
- **Types**: Use Pydantic models/schemas for data validation; add return type hints
- **Error handling**: Use try/except blocks for API calls with descriptive messages
- **Documentation**: Add docstrings to functions explaining purpose/parameters/returns
- **Organization**: 
  - Keep integration clients in separate modules
  - Use dependency injection for services in FastAPI
- **Configuration**: Use pydantic_settings for env variables, never hardcode secrets

## Development Workflow
- Use FastAPI's dependency injection pattern for service integrations
- Build new dashboard widgets as separate components
- Test API integrations using CLI tests before implementing in main app
- Use Pydantic for data validation and schema definitions
- Implement async functionality where appropriate for better performance
- Handle API errors gracefully with user-friendly messages
- Consider caching strategies for API rate limits