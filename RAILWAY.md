# Railway Deployment

This project is ready for one-click deployment on Railway.

## Configuration Files:
- `railway.toml`: Build and start settings.
- `Procfile`: Process definition for Railway/Heroku.
- `build.sh`: Installation, static collection, and migrations.

## Database:
The app uses `dj-database-url` to naturally connect to Railway's PostgreSQL. Just add a PostgreSQL service to your project and Railway handles the rest.

Refer to the [Railway Guide](file:///C:/Users/Dipak/.gemini/antigravity/brain/91d97901-354f-4b64-8926-b15e85d6aa61/railway_guide.md) for detailed steps.
