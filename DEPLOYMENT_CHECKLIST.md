# Deployment Checklist

## Pre-Deployment
- [ ] Code is committed to Git repository
- [ ] All tests pass locally
- [ ] Database scripts are ready

## Backend Deployment
- [ ] Choose platform (Render or Railway)
- [ ] Create PostgreSQL database service
- [ ] Deploy backend service
- [ ] Set environment variables:
  - [ ] `DATABASE_URL`
  - [ ] `FRONTEND_URL` (set after frontend deployment)
- [ ] Test backend endpoints
- [ ] Run database setup scripts

## Frontend Deployment
- [ ] Deploy frontend service
- [ ] Update `config.js` with production backend URL
- [ ] Test frontend functionality
- [ ] Update backend `FRONTEND_URL` environment variable

## Post-Deployment
- [ ] Test complete user flow
- [ ] Verify music playback works
- [ ] Check mobile responsiveness
- [ ] Monitor error logs
- [ ] Set up monitoring/analytics (optional)

## URLs to Update
- [ ] Backend: Update `FRONTEND_URL` in environment variables
- [ ] Frontend: Update `PRODUCTION_API` in `config.js`
- [ ] CORS: Verify frontend domain is allowed

## Database Setup Commands
```bash
# After deployment, run these with your production DATABASE_URL
python import_setup.py
python import_data_postgresql.py
python add_sample_votes.py
```
