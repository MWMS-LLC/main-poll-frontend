# 🚀 Teen Poll App Deployment Checklist

## Backend Deployment (Render)

### ✅ Pre-deployment Checks
- [ ] All code changes committed and pushed to repository
- [ ] `main_production.py` is updated and working
- [ ] `Procfile` points to `main_production:app`
- [ ] Database schema files are ready (`schema_setup.sql`, `schema_results.sql`)
- [ ] Environment variables configured in Render dashboard

### 🔧 Environment Variables (Render Dashboard)
Set these in your Render service dashboard:

```
DATABASE_URL=postgresql://username:password@host:port/database
```

**Important:** The DATABASE_URL should be in this format:
- `postgresql://` (not `postgres://`)
- Include username, password, host, port, and database name
- Example: `postgresql://myuser:mypassword@myhost.com:5432/mydatabase`

### 📊 Database Setup
1. **Create PostgreSQL database** in Render or external provider
2. **Run schema setup**:
   ```sql
   -- First run schema_setup.sql
   -- Then run schema_results.sql
   ```
3. **Import data** from CSV files:
   - `categories.csv`
   - `blocks.csv` 
   - `questions.csv`
   - `options.csv`
   - `soundtracks.csv`

### 🚀 Deploy to Render
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main_production:app --host 0.0.0.0 --port $PORT`
4. Deploy and monitor logs

### 🧪 Post-deployment Testing
- [ ] Test `/health` endpoint
- [ ] Test `/api/categories` endpoint
- [ ] Test database connection
- [ ] Verify all API endpoints work

## Frontend Deployment (Vercel/Netlify)

### ✅ Pre-deployment Checks
- [ ] All code changes committed and pushed
- [ ] `config.js` points to correct backend URL
- [ ] All components working locally
- [ ] No console errors

### 🔧 Configuration
- [ ] Update `frontend/src/config.js` with production backend URL
- [ ] Ensure CORS is properly configured in backend

### 🚀 Deploy Frontend
1. Connect repository to Vercel/Netlify
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy and test

## 🧪 End-to-End Testing

### ✅ User Flow Testing
- [ ] Landing page loads with 12 category buttons
- [ ] Age verification modal appears for new users
- [ ] Category page shows blocks
- [ ] Block page shows questions
- [ ] Voting works (single choice and checkbox)
- [ ] Results display correctly
- [ ] Validation messages appear
- [ ] Companion advice works

### 🔍 Debugging Common Issues

#### Backend Issues
- **DATABASE_URL parsing error**: Check URL format and special characters
- **Connection refused**: Verify database is running and accessible
- **Table not found**: Run schema files in correct order

#### Frontend Issues
- **CORS errors**: Check backend CORS configuration
- **API calls failing**: Verify backend URL and endpoints
- **Styling issues**: Check CSS animations and responsive design

## 📱 Mobile Testing
- [ ] Test on mobile devices
- [ ] Verify touch interactions work
- [ ] Check responsive design
- [ ] Test on different screen sizes

## 🔒 Security & Performance
- [ ] Environment variables are secure
- [ ] No sensitive data in client-side code
- [ ] API rate limiting (if needed)
- [ ] Database connection pooling
- [ ] Error handling and logging

## 📊 Monitoring
- [ ] Set up logging in Render dashboard
- [ ] Monitor API response times
- [ ] Track database performance
- [ ] Set up alerts for errors

---

## 🆘 Troubleshooting

### Common Error: "Failed to parse DATABASE_URL"
**Solution**: Ensure DATABASE_URL format is correct:
```
✅ Correct: postgresql://user:pass@host:port/db
❌ Wrong: postgres://user:pass@host:port/db
❌ Wrong: postgresql://user@host:port/db (missing password)
```

### Common Error: "Could not establish database connection"
**Solutions**:
1. Check if database is running
2. Verify network access from Render
3. Check firewall settings
4. Verify credentials

### Common Error: "Table does not exist"
**Solution**: Run schema files in order:
1. `schema_setup.sql` (creates core tables)
2. `schema_results.sql` (creates results tables)
3. Import CSV data

---

**Need help?** Check the Render logs and ensure all environment variables are set correctly!
