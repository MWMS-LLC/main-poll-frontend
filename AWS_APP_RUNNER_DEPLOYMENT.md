# AWS App Runner Deployment Guide for My World My Say Backend

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **RDS PostgreSQL Database** already set up (based on your existing setup)
3. **AWS CLI** configured with your credentials
4. **Git repository** with your code

## Database Setup

Your database is already configured at:
- Host: `database-1.c320aqgmywbc.us-east-2.rds.amazonaws.com`
- Port: `5432`
- Database: `postgres`
- User: `postgres`
- Password: `NBem0YTOfN94yKqFSw5F`

## Environment Variables for App Runner

You'll need to set these environment variables in AWS App Runner:

```
DB_HOST=database-1.c320aqgmywbc.us-east-2.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=NBem0YTOfN94yKqFSw5F
PORT=8080
LOG_LEVEL=INFO
FRONTEND_URL=https://your-frontend-domain.com
```

## Deployment Steps

### 1. Test Locally First

```bash
# Navigate to your project directory
cd /Users/1withyin/dev/teen0909

# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
export DB_HOST=database-1.c320aqgmywbc.us-east-2.rds.amazonaws.com
export DB_PORT=5432
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=NBem0YTOfN94yKqFSw5F
export PORT=8080

# Run the application
python backend/main.py
```

### 2. Deploy to AWS App Runner

1. **Go to AWS App Runner Console**
   - Navigate to AWS App Runner in your AWS Console
   - Click "Create service"

2. **Source Configuration**
   - Choose "Source code repository"
   - Connect your GitHub repository
   - Select the branch (usually `main`)
   - Build type: "App Runner configuration file"

3. **Service Configuration**
   - Service name: `myworldmysay-backend` (or your preferred name)
   - Virtual CPU: 0.25 vCPU
   - Virtual memory: 0.5 GB
   - Environment variables: Add all the environment variables listed above

4. **Auto Scaling**
   - Min size: 1
   - Max size: 10
   - Concurrency: 100

5. **Health Check**
   - Health check path: `/health`
   - Health check interval: 20 seconds
   - Health check timeout: 2 seconds
   - Healthy threshold: 1
   - Unhealthy threshold: 5

6. **Create and Deploy**
   - Click "Create & deploy"
   - Wait for the deployment to complete (usually 5-10 minutes)

## Testing the Deployment

Once deployed, you can test your endpoints:

1. **Health Check**: `https://your-app-url/health`
2. **Database Check**: `https://your-app-url/db-check`
3. **Categories**: `https://your-app-url/api/categories`

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify RDS security groups allow connections from App Runner
   - Check that the database is publicly accessible or in the same VPC

2. **Build Failures**
   - Check the build logs in App Runner console
   - Ensure all dependencies are in requirements.txt

3. **Runtime Errors**
   - Check the application logs in App Runner console
   - Verify all environment variables are set correctly

### Security Considerations

1. **Database Security**
   - Consider using AWS Secrets Manager for database credentials
   - Ensure RDS is in a private subnet with proper security groups

2. **Environment Variables**
   - Never commit sensitive data to your repository
   - Use AWS Secrets Manager or Parameter Store for production secrets

## Monitoring

- **CloudWatch Logs**: Application logs are automatically sent to CloudWatch
- **CloudWatch Metrics**: Monitor CPU, memory, and request metrics
- **Health Checks**: Monitor application health through the `/health` endpoint

## Next Steps

1. Set up a custom domain for your App Runner service
2. Configure SSL/TLS certificates
3. Set up monitoring and alerting
4. Implement CI/CD pipeline for automated deployments
