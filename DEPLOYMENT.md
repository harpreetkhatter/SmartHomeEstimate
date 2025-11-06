# Delhi House Price Predictor - Deployment Guide

## Option 1: Heroku Deployment (Recommended)

### Prerequisites
1. Install Git: https://git-scm.com/downloads
2. Create Heroku account: https://signup.heroku.com/
3. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

### Steps:

1. **Initialize Git repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

4. **Open your app**
   ```bash
   heroku open
   ```

## Option 2: Railway Deployment

1. Go to https://railway.app/
2. Connect your GitHub repository
3. Deploy automatically

## Option 3: Render Deployment

1. Go to https://render.com/
2. Connect your GitHub repository
3. Choose "Web Service"
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn --chdir server server:app`

## Option 4: Local Testing

Run locally:
```bash
cd server
python server.py
```

Visit: http://localhost:5000

## Files Created for Deployment:
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku process file
- Updated `server.py` - Production-ready Flask app
- Updated `util.py` - Fixed file paths

## Important Notes:
- Model files are copied to server/artifacts/
- HTML is served from Flask backend
- CORS is enabled for API calls
- Production-ready configuration