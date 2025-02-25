# CLAUDE.md: Rhino App Development Guidelines

## Application Commands
- Run Flask app: `python app.py`
- Run FastAPI app: `python -m app.main` or `uvicorn app.main:app --reload`
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
- Focus on the FastAPI app in the app/ directory for new development
- Test API integrations using CLI tests before implementing in main app
- Use Pydantic for data validation and schema definitions
- Follow FastAPI dependency injection patterns for services
- Handle API errors gracefully with user-friendly messages