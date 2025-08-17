# Deployment Guide

This guide will help you deploy your Teen Poll app to either Render or Railway.

## Prerequisites

1. **Database**: You'll need a PostgreSQL database. Both Render and Railway offer PostgreSQL services.
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Option 1: Deploy to Render

### Backend Deployment

1. **Sign up/Login to Render**: Go to [render.com](https://render.com)

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Select the repository with your Teen Poll app

3. **Configure the service**:
   - **Name**: `teen-poll-backend` (or your preferred name)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `FRONTEND_URL`: Your frontend URL (set this after deploying frontend)

5. **Database Setup**:
   - Create a new PostgreSQL service in Render
   - Copy the connection string to your backend's `DATABASE_URL`
   - Run your database setup scripts (import_data_postgresql.py, etc.)

### Frontend Deployment

1. **Create a new Static Site**:
   - Click "New +" → "Static Site"
   - Connect your Git repository

2. **Configure the service**:
   - **Name**: `teen-poll-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

3. **Environment Variables**:
   - Update your frontend's API calls to use the backend URL

## Option 2: Deploy to Railway

### Backend Deployment

1. **Sign up/Login to Railway**: Go to [railway.app](https://railway.app)

2. **Create a new project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure the service**:
   - Railway will automatically detect it's a Python app
   - The `railway.json` file will handle the configuration

4. **Environment Variables**:
   - Add `DATABASE_URL` in the Variables tab
   - Add `FRONTEND_URL` after deploying frontend

5. **Database Setup**:
   - Create a new PostgreSQL service in Railway
   - Connect it to your backend service
   - Run your database setup scripts

### Frontend Deployment

1. **Create a new service**:
   - Click "New Service" → "Static Site"
   - Connect your Git repository

2. **Configure the service**:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Output Directory**: `dist`

## Database Setup

After deploying your backend, you'll need to set up your database:

1. **Connect to your deployed database** using the connection string
2. **Run your setup scripts**:
   ```bash
   # You may need to run these locally with the remote DATABASE_URL
   python import_setup.py
   python import_data_postgresql.py
   python add_sample_votes.py
   ```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `FRONTEND_URL`: Your frontend domain for CORS
- `PORT`: Automatically set by the platform

### Frontend
- Update `config.js` to use your backend URL instead of localhost

## CORS Configuration

Your backend is already configured to allow all origins (`allow_origins=["*"]`). In production, you should restrict this to your frontend domain:

```python
# In main.py, update the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing

After deployment:
1. Test your backend API endpoints
2. Test your frontend functionality
3. Verify database connections
4. Test the complete user flow

## Troubleshooting

- **Database connection issues**: Check your `DATABASE_URL` format
- **Build failures**: Check the build logs for missing dependencies
- **CORS errors**: Verify your `FRONTEND_URL` is correct
- **Port issues**: Make sure your app binds to `0.0.0.0` and uses `$PORT`

## Cost Considerations

- **Render**: Free tier available, then $7/month for web services
- **Railway**: Pay-as-you-use pricing, typically $5-20/month for small apps

Both platforms offer generous free tiers for development and testing.
