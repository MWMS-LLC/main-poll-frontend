import csv
import os
import sys
import uuid
from db import execute_query, execute_many, execute_script
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_csv_value(value):
    """Clean CSV values by removing BOM and handling multi-line content"""
    if value is None:
        return ''
    # Remove BOM and clean whitespace
    cleaned = str(value).replace('\ufeff', '').strip()
    # Handle multi-line content by replacing newlines with spaces
    cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
    return cleaned

def load_csv_data():
    """Load CSV data into the database"""
    
    # First, run the schema setup
    logger.info("Setting up database schema...")
    try:
        with open('schema_setup.sql', 'r') as f:
            setup_sql = f.read()
        
        # Execute the entire schema as one block instead of splitting by semicolons
        logger.info("Executing schema setup...")
        try:
            execute_script(setup_sql)
            logger.info("Schema setup completed successfully")
        except Exception as e:
            logger.error(f"Schema setup failed: {e}")
            return False
        
    except Exception as e:
        logger.error(f"Schema setup failed: {e}")
        return False
    
    # Load categories
    logger.info("Loading categories...")
    try:
        with open('../data/categories.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean all values
                clean_row = {clean_csv_value(k): clean_csv_value(v) for k, v in row.items()}
                
                query = """
                INSERT INTO categories (id, category_name, description, category_text, category_text_long, version, uuid)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                execute_query(query, (
                    int(clean_row['id']),
                    clean_row['category_name'],
                    clean_row.get('description', ''),
                    clean_row.get('category_text', ''),
                    clean_row.get('category_text_long', ''),
                    clean_row.get('version', '1'),
                    clean_row['uuid']
                ), fetch=False)
        logger.info("Categories loaded successfully")
    except Exception as e:
        logger.error(f"Categories loading failed: {e}")
        return False
    
    # Load blocks
    logger.info("Loading blocks...")
    try:
        with open('../data/blocks.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean all values
                clean_row = {clean_csv_value(k): clean_csv_value(v) for k, v in row.items()}
                
                query = """
                INSERT INTO blocks (id, category_id, block_number, block_code, block_text, version, uuid)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                execute_query(query, (
                    int(clean_row['id']),
                    int(clean_row['category_id']),
                    int(clean_row['block_number']),
                    clean_row['block_code'],
                    clean_row['block_text'],
                    clean_row.get('version', '1'),
                    clean_row['uuid']
                ), fetch=False)
        logger.info("Blocks loaded successfully")
    except Exception as e:
        logger.error(f"Blocks loading failed: {e}")
        return False
    
    # Load questions
    logger.info("Loading questions...")
    try:
        with open('../data/questions.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean all values
                clean_row = {clean_csv_value(k): clean_csv_value(v) for k, v in row.items()}
                
                query = """
                INSERT INTO questions (id, question_code, question_number, question_text, category_id, block_number, 
                                    is_start_question, check_box, color_code, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                execute_query(query, (
                    int(clean_row['id']),
                    clean_row['question_code'],
                    int(clean_row['question_number']),
                    clean_row['question_text'],
                    int(clean_row['category_id']),
                    int(clean_row['block_number']) if clean_row['block_number'] else None,
                    1 if clean_row['is_start_question'].upper() == 'TRUE' else 0,
                    1 if clean_row['check_box'].upper() == 'TRUE' else 0,
                    clean_row.get('color_code', ''),
                    clean_row.get('version', '1')
                ), fetch=False)
        logger.info("Questions loaded successfully")
    except Exception as e:
        logger.error(f"Questions loading failed: {e}")
        return False
    
    # Load options
    logger.info("Loading options...")
    try:
        with open('../data/options.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean all values
                clean_row = {clean_csv_value(k): clean_csv_value(v) for k, v in row.items()}
                
                query = """
                INSERT INTO options (id, question_code, option_text, option_select, option_code, 
                                   next_question_code, response_message, companion_advice, tone_tag, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                execute_query(query, (
                    int(clean_row['id']),
                    clean_row['question_code'],
                    clean_row['option_text'],
                    clean_row['option_select'],
                    clean_row['option_code'],
                    clean_row.get('next_question_code', ''),
                    clean_row.get('response_message', ''),
                    clean_row.get('companion_advice', ''),
                    clean_row.get('tone_tag', ''),
                    clean_row.get('version', '1')
                ), fetch=False)
        logger.info("Options loaded successfully")
    except Exception as e:
        logger.error(f"Options loading failed: {e}")
        return False
    
    # Now run the results schema
    logger.info("Setting up results schema...")
    try:
        with open('schema_results.sql', 'r') as f:
            results_sql = f.read()
        
        # Execute the entire results schema as one block
        logger.info("Executing results schema...")
        try:
            execute_script(results_sql)
            logger.info("Results schema setup completed successfully")
        except Exception as e:
            logger.error(f"Results schema setup failed: {e}")
            return False
        
    except Exception as e:
        logger.error(f"Results schema setup failed: {e}")
        return False
    
    logger.info("Data import completed successfully!")
    return True

if __name__ == "__main__":
    success = load_csv_data()
    if success:
        logger.info("All data imported successfully!")
        sys.exit(0)
    else:
        logger.error("Data import failed!")
        sys.exit(1)
