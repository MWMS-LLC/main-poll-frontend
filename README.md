# My World My Say - Teen Poll Application

## Project Structure

```
main0908/
├── aws-scripts/           # AWS deployment and setup scripts
│   ├── setup_database_complete.py
│   └── import_to_aws.py
├── database-scripts/      # Database schema files
│   ├── schema_setup.sql
│   └── schema_results.sql
├── cleanup-scripts/       # Project maintenance scripts
│   └── cleanup_unused_files.py
├── data/                  # CSV data files
│   ├── categories.csv
│   ├── blocks.csv
│   ├── questions.csv
│   └── options.csv
├── backend/               # Backend application code
└── frontend/              # Frontend application code
```

## Database Setup

The application uses AWS RDS PostgreSQL with the following tables:

### Setup Tables (Static Data)
- `categories` - Survey categories
- `blocks` - Question blocks
- `questions` - Survey questions
- `options` - Answer options

### Results Tables (Dynamic Data)
- `users` - User information
- `responses` - Single-choice responses
- `checkbox_responses` - Multi-select responses
- `other_responses` - Free-text responses

## Quick Start

1. **Set up database:**
   ```bash
   python3 aws-scripts/setup_database_complete.py
   ```

2. **Deploy frontend:**
   - Use AWS Amplify to deploy from GitHub repositories
   - Main site: `MWMSLLC/main-poll-frontend`
   - Teen site: `MWMSLLC/teen-poll-frontend`

3. **Deploy backend:**
   - Use AWS Lambda or Elastic Beanstalk
   - Connect to RDS database

## Subdomain Architecture

- `myworldmysay.com` → Main site (main-poll-frontend + main-poll-backend)
- `teen.myworldmysay.com` → Teen site (teen-poll-frontend + teen-poll-backend)
- Each subdomain has its own database and separate data

## AWS Resources

- **RDS Database:** `database-1.c320aqgmywbc.us-east-2.rds.amazonaws.com`
- **Region:** us-east-2 (Ohio)
- **Database:** postgres
- **User:** postgres

## Development

This project supports multiple subdomains with separate frontend/backend/database for each, allowing for different user experiences and data isolation.
