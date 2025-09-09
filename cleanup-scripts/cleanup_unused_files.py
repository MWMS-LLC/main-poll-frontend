#!/usr/bin/env python3
"""
Cleanup script to remove unused files and organize the project structure.
"""

import os
import shutil
from pathlib import Path

def cleanup_backend_files():
    """Remove unused backend files"""
    backend_dir = Path("backend")
    
    # Files to remove (keep only essential ones)
    files_to_remove = [
        "import_setup.py",
        "import_to_render.py", 
        "import_data_only.py",
        "create_schema_step_by_step.py",
        "check_tables.py",
        "add_day_of_week_text_column.py",
        "simple_test_connection.py",
        "import_data_simple.py",
        "create_schema_local.py",
        "import_data_local.py",
        "create_schema.py",
        "check_schema.py",
        "import_setup_fixed.py",
        "import_to_render_fixed.py",
        "create_schema_render.py",
        "add_column_render.py",
        "reset_render_db.py",
        "test_render_connection.py",
        "test_connection.py",
        "test_db_connection.py",
        "test_upload.py",
        "test_weekday_logic.py",
        "test_weekday_simple.py",
        "test_checkbox_connection.py",
        "simple_test.py",
        "demo_progress.py",
        "main_local_duplicate.py",
        "main_local.py",
        "main_production.py",
        "import_soundtracks.py",
        "import_to_render.py",
        "clean_option_prefixes.py"
    ]
    
    removed_count = 0
    for file in files_to_remove:
        file_path = backend_dir / file
        if file_path.exists():
            file_path.unlink()
            print(f"🗑️  Removed: {file}")
            removed_count += 1
    
    print(f"✅ Removed {removed_count} unused files from backend/")

def organize_data_files():
    """Organize data files"""
    data_dir = Path("data")
    if data_dir.exists():
        print("📁 Data directory structure:")
        for file in data_dir.iterdir():
            if file.is_file():
                size = file.stat().st_size
                print(f"  📄 {file.name} ({size:,} bytes)")

def create_readme():
    """Create a comprehensive README for the project"""
    readme_content = """# My World My Say - Teen Poll Application

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
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("📝 Created comprehensive README.md")

def main():
    """Main cleanup function"""
    print("🧹 Starting project cleanup...")
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    
    # Clean up backend files
    cleanup_backend_files()
    
    # Organize data files
    organize_data_files()
    
    # Create README
    create_readme()
    
    print("\n✅ Project cleanup completed!")
    print("📁 Project is now organized and ready for deployment!")

if __name__ == "__main__":
    main()
