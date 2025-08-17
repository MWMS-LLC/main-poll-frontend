from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pg8000
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging - force it to be very verbose
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

# Force print statements to flush immediately
import sys
sys.stdout.flush()
sys.stderr.flush()

# Initialize FastAPI app
app = FastAPI(title="Teen Poll API", version="1.0.0")

# Add startup message
logger.info("🚀 TEEN POLL API STARTING UP - DEBUG LOGGING TEST!")
print("🚀 TEEN POLL API STARTING UP - PRINT STATEMENT TEST!")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    """Get database connection"""
    try:
        # For local testing, use local database
        # For production, use DATABASE_URL environment variable
        if os.getenv("ENVIRONMENT") == "production":
            database_url = os.getenv("DATABASE_URL")
            logger.info(f"Attempting to connect to production database with URL: {database_url}")
            
            if not database_url:
                logger.error("DATABASE_URL environment variable is not set!")
                return None
            
            # Use the correct database connection parameters from Render
            host = "dpg-d2gfof75r7bs73f1uc0g-a"
            port = 5432
            database = "mwms_teen_poll"
            user = "mwms_teen_poll_user"
            password = "CTF1UxZpzk4E2vhevF5GE3NEAuFBxPiF"
            
            logger.info(f"Using production connection: host={host}, port={port}, database={database}, user={user}")
        else:
            # Local development - use local PostgreSQL
            host = "localhost"
            port = 5432
            database = "teen_poll"
            user = "1withyin"  # Your local username
            password = ""  # No password for local
            logger.info(f"Using local connection: host={host}, port={port}, database={database}, user={user}")
        
        conn = pg8000.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        logger.info("Database connection successful!")
        return conn
            
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

# Database query execution function
def execute_query(query: str, params: tuple = None, fetch: bool = True):
    """Execute database query"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not establish database connection")
        
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            # Fetch all rows and convert to list of dicts
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            return results
        else:
            conn.commit()
            return True
            
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed: {e}")
    finally:
        if conn:
            conn.close()

@app.on_event("startup")
async def startup_event():
    """Initialize database connection pool on startup"""
    # The original code had db_pool, but it's removed.
    # This function is kept as it was not explicitly removed by the new_code.
    # However, the new_code removed the db_pool logic.
    # This function will now effectively do nothing if db_pool is removed.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection pool on shutdown"""
    # The original code had db_pool, but it's removed.
    # This function is kept as it was not explicitly removed by the new_code.
    # However, the new_code removed the db_pool logic.
    # This function will now effectively do nothing if db_pool is removed.
    pass

# Request validation functions (replacing pydantic)
def validate_user_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate user creation request"""
    if not isinstance(data.get('user_uuid'), str):
        raise HTTPException(status_code=400, detail="user_uuid must be a string")
    if not isinstance(data.get('year_of_birth'), int):
        raise HTTPException(status_code=400, detail="year_of_birth must be an integer")
    return data

def validate_vote_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate vote request"""
    if not isinstance(data.get('question_code'), str):
        raise HTTPException(status_code=400, detail="question_code must be a string")
    if not isinstance(data.get('option_select'), str):
        raise HTTPException(status_code=400, detail="option_select must be a string")
    if not isinstance(data.get('user_uuid'), str):
        raise HTTPException(status_code=400, detail="user_uuid must be a string")
    return data

def validate_checkbox_vote_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate checkbox vote request"""
    if not isinstance(data.get('question_code'), str):
        raise HTTPException(status_code=400, detail="question_code must be a string")
    if not isinstance(data.get('option_selects'), list):
        raise HTTPException(status_code=400, detail="option_selects must be a list")
    if not isinstance(data.get('user_uuid'), str):
        raise HTTPException(status_code=400, detail="user_uuid must be a string")
    return data

def validate_other_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate other text request"""
    if not isinstance(data.get('question_code'), str):
        raise HTTPException(status_code=400, detail="question_code must be a string")
    if not isinstance(data.get('user_uuid'), str):
        raise HTTPException(status_code=400, detail="user_uuid must be a string")
    if not isinstance(data.get('other_text'), str):
        raise HTTPException(status_code=400, detail="other_text must be a string")
    return data

# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Teen Poll API is running", "status": "ok"}

@app.get("/test")
async def test():
    """Test endpoint to verify code is running"""
    print("🔍 PRINT: Test endpoint called!")
    logger.info("🔍 Test endpoint called - debug logging is working!")
    logger.error("🔍 ERROR: Test endpoint called - error logging test!")
    logger.debug("🔍 DEBUG: Test endpoint called - debug logging test!")
    return {"message": "Test endpoint working", "timestamp": str(datetime.now())}

@app.get("/health")
async def health():
    """Health check endpoint that doesn't require database"""
    return {"status": "healthy", "timestamp": str(datetime.datetime.now())}

@app.get("/api/categories")
async def get_categories():
    """Get all categories"""
    print("🔍 PRINT: Categories endpoint called!")
    logger.info("🔍 LOG: Categories endpoint called!")
    
    try:
        print("🔍 PRINT: About to execute database query")
        logger.info("🔍 LOG: About to execute database query")
        
        query = "SELECT * FROM categories ORDER BY id"
        results = execute_query(query)
        
        print(f"🔍 PRINT: Query successful, got {len(results)} results")
        logger.info(f"🔍 LOG: Query successful, got {len(results)} results")
        
        return results
    except Exception as e:
        print(f"🔍 PRINT: Error in categories endpoint: {e}")
        logger.error(f"🔍 LOG: Error in categories endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@app.get("/api/categories/{category_id}/blocks")
async def get_blocks_by_category(category_id: int):
    """Get blocks for a specific category"""
    query = "SELECT * FROM blocks WHERE category_id = %s ORDER BY block_number"
    results = execute_query(query, (category_id,))
    return results

@app.get("/api/blocks/{block_code}/questions")
async def get_questions_by_block(block_code: str):
    """Get questions for a specific block"""
    # Extract category_id and block_number from block_code (e.g., "1_1" -> category_id=1, block_number=1)
    try:
        parts = block_code.split('_')
        if len(parts) == 2:
            category_id = int(parts[0])
            block_number = int(parts[1])
        else:
            raise ValueError("Invalid block_code format")
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid block_code format. Expected format: category_block (e.g., 1_1)")
    
    query = "SELECT * FROM questions WHERE category_id = %s AND block_number = %s ORDER BY question_number"
    results = execute_query(query, (category_id, block_number))
    return results

@app.get("/api/questions/{question_code}/options")
async def get_options_by_question(question_code: str):
    """Get options for a specific question"""
    query = "SELECT * FROM options WHERE question_code = %s ORDER BY option_select"
    results = execute_query(query, (question_code,))
    return results

@app.post("/api/users")
async def create_user(user: Dict[str, Any]):
    """Create a new user with age validation"""
    try:
        validated_data = validate_user_request(user)
        # Validate age (2007-2012)
        if validated_data['year_of_birth'] < 2007 or validated_data['year_of_birth'] > 2012:
            raise HTTPException(status_code=400, detail="Invalid year of birth. Must be between 2007-2012.")
        
        query = """
            INSERT INTO users (user_uuid, year_of_birth, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_uuid) DO NOTHING
        """
        execute_query(query, (validated_data['user_uuid'], validated_data['year_of_birth'], datetime.now()), fetch=False)
        return {"message": "User created successfully", "user_uuid": validated_data['user_uuid']}
    except Exception as e:
        logger.error(f"User creation failed: {e}")
        raise HTTPException(status_code=500, detail="User creation failed")

@app.get("/api/users")
async def get_users():
    """Get all users (for debugging)"""
    query = "SELECT user_uuid, year_of_birth, created_at FROM users"
    results = execute_query(query)
    return {"users": results}

@app.post("/api/vote")
async def vote(vote_data: Dict[str, Any]):
    """Record a single-choice vote"""
    try:
        logger.info(f"Received vote request: {vote_data}")
        
        # Get question and category details for denormalization
        question_query = """
            SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            WHERE q.question_code = %s
        """
        question_info = execute_query(question_query, (vote_data['question_code'],))
        
        if not question_info:
            logger.error(f"Question not found: {vote_data['question_code']}")
            raise HTTPException(status_code=404, detail="Question not found")
        
        question = question_info[0]
        logger.info(f"Question info: {question}")
        
        # Get option details
        option_query = """
            SELECT option_text, option_code
            FROM options
            WHERE question_code = %s AND option_select = %s
        """
        option_info = execute_query(option_query, (vote_data['question_code'], vote_data['option_select']))
        
        if not option_info:
            logger.error(f"Option not found: question_code={vote_data['question_code']}, option_select={vote_data['option_select']}")
            raise HTTPException(status_code=404, detail="Option not found")
        
        option = option_info[0]
        logger.info(f"Option info: {option}")
        
        # Insert vote with denormalized data
        insert_query = """
            INSERT INTO responses (
                question_code, option_select, option_code, option_text, user_uuid,
                question_text, question_number, category_name, category_id, block_number, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(insert_query, (
            vote_data['question_code'], vote_data['option_select'], option['option_code'], option['option_text'],
            vote_data['user_uuid'], question['question_text'], question['question_number'],
            question['category_name'], question['category_id'], question['block_number'], datetime.now()
        ), fetch=False)
        
        logger.info(f"Vote recorded successfully for user {vote_data['user_uuid']}")
        return {"message": "Vote recorded successfully"}
        
    except Exception as e:
        logger.error(f"Vote recording failed: {e}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception details: {str(e)}")
        raise HTTPException(status_code=500, detail="Vote recording failed")

@app.post("/api/checkbox_vote")
async def checkbox_vote(vote_data: Dict[str, Any]):
    """Record a checkbox vote with weights"""
    try:
        # Get question and category details for denormalization
        question_query = """
            SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            WHERE q.question_code = %s
        """
        question_info = execute_query(question_query, (vote_data['question_code'],))
        
        if not question_info:
            raise HTTPException(status_code=404, detail="Question not found")
        
        question = question_info[0]
        
        # Calculate weight for each option
        weight = 1.0 / len(vote_data['option_selects'])
        
        # Insert votes for each selected option
        for option_select in vote_data['option_selects']:
            # Handle "OTHER" option specially for checkbox questions
            if option_select == "OTHER":
                # For "OTHER" in checkbox questions, we need to get the actual text
                # This should come from the frontend as a separate field
                other_text = vote_data.get('other_text', 'OTHER')
                
                # Insert "OTHER" as a checkbox response with proper weight
                insert_query = """
                    INSERT INTO checkbox_responses (
                        question_code, option_select, option_code, option_text, user_uuid,
                        question_text, question_number, category_name, category_id, block_number, weight, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_query(insert_query, (
                    vote_data['question_code'], "OTHER", "OTHER", other_text,
                    vote_data['user_uuid'], question['question_text'], question['question_number'],
                    question['category_name'], question['category_id'], question['block_number'], weight, datetime.now()
                ), fetch=False)
            else:
                # Get option details for regular options
                option_query = """
                    SELECT option_text, option_code
                    FROM options
                    WHERE question_code = %s AND option_select = %s
                """
                option_info = execute_query(option_query, (vote_data['question_code'], option_select))
                
                if not option_info:
                    continue  # Skip invalid options
                
                option = option_info[0]
                
                # Insert checkbox vote with denormalized data
                insert_query = """
                    INSERT INTO checkbox_responses (
                        question_code, option_select, option_code, option_text, user_uuid,
                        question_text, question_number, category_name, category_id, block_number, weight, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_query(insert_query, (
                    vote_data['question_code'], option_select, option['option_code'], option['option_text'],
                    vote_data['user_uuid'], question['question_text'], question['question_number'],
                    question['category_name'], question['category_id'], question['block_number'], weight, datetime.now()
                ), fetch=False)
        
        return {"message": "Checkbox vote recorded successfully"}
        
    except Exception as e:
        logger.error(f"Checkbox vote recording failed: {e}")
        raise HTTPException(status_code=500, detail="Checkbox vote recording failed")

@app.post("/api/other")
async def submit_other(other_data: Dict[str, Any]):
    """Record a free-text response"""
    try:
        # Get question and category details for denormalization
        question_query = """
            SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            WHERE q.question_code = %s
        """
        question_info = execute_query(question_query, (other_data['question_code'],))
        
        if not question_info:
            raise HTTPException(status_code=404, detail="Question not found")
        
        question = question_info[0]
        
        # Insert other response with denormalized data
        insert_query = """
            INSERT INTO other_responses (
                question_code, user_uuid, other_text, question_text, question_number,
                category_name, category_id, block_number, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(insert_query, (
            other_data['question_code'], other_data['user_uuid'], other_data['other_text'],
            question['question_text'], question['question_number'], question['category_name'],
            question['category_id'], question['block_number'], datetime.now()
        ), fetch=False)
        
        return {"message": "Other response recorded successfully"}
        
    except Exception as e:
        logger.error(f"Other response recording failed: {e}")
        raise HTTPException(status_code=500, detail="Other response recording failed")

@app.get("/api/soundtracks")
async def get_soundtracks():
    """Get all soundtracks"""
    try:
        query = """
        SELECT song_id, song_title, mood_tag, playlist_tag, lyrics_snippet, 
               featured, featured_order, file_url
        FROM soundtracks 
        ORDER BY featured_order, song_title
        """
        results = execute_query(query)
        logger.info(f"Retrieved {len(results)} soundtracks")
        return {"soundtracks": results}
    except Exception as e:
        logger.error(f"Error retrieving soundtracks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve soundtracks: {str(e)}")

@app.get("/api/soundtracks/playlists")
async def get_playlists():
    """Get all unique playlists"""
    try:
        query = """
        SELECT DISTINCT unnest(string_to_array(playlist_tag, ', ')) as playlist
        FROM soundtracks 
        WHERE playlist_tag IS NOT NULL AND playlist_tag != ''
        ORDER BY playlist
        """
        results = execute_query(query)
        playlists = ['All Songs'] + [r['playlist'] for r in results]
        logger.info(f"Retrieved {len(playlists)} playlists")
        return {"playlists": playlists}
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve playlists: {str(e)}")

@app.get("/api/results/{question_code}")
async def get_results(question_code: str):
    """Get results for a specific question"""
    try:
        # Check if it's a checkbox question by looking at the question type
        question_query = "SELECT * FROM questions WHERE question_code = %s"
        question_info = execute_query(question_query, (question_code,))
        
        if not question_info:
            raise HTTPException(status_code=404, detail="Question not found")
        
        question = question_info[0]
        
        # For now, assume all questions can have both types of responses
        # Get single-choice responses
        single_query = """
            SELECT option_select, COUNT(*) as count
            FROM responses
            WHERE question_code = %s
            GROUP BY option_select
            ORDER BY option_select
        """
        single_results = execute_query(single_query, (question_code,))
        
        # Get checkbox responses (sum of weights)
        checkbox_query = """
            SELECT option_select, SUM(weight) as count
            FROM checkbox_responses
            WHERE question_code = %s
            GROUP BY option_select
            ORDER BY option_select
        """
        checkbox_results = execute_query(checkbox_query, (question_code,))
        
        # Get OTHER responses with proper weighting
        other_query = """
            SELECT COUNT(*) as count
            FROM other_responses
            WHERE question_code = %s
        """
        other_results = execute_query(other_query, (question_code,))
        
        # Combine results
        all_results = {}
        
        # Add single-choice results
        for result in single_results:
            option = result['option_select']
            if option in all_results:
                all_results[option]['count'] += result['count']
            else:
                all_results[option] = {'option_select': option, 'count': result['count']}
        
        # Add checkbox results
        for result in checkbox_results:
            option = result['option_select']
            if option in all_results:
                all_results[option]['count'] += result['count']
            else:
                all_results[option] = {'option_select': option, 'count': result['count']}
        
        # Add OTHER responses with proper weighting
        if other_results and other_results[0]['count'] > 0:
            other_count = other_results[0]['count']
            # For OTHER responses, we need to check if they came from checkbox questions
            # and apply the same weighting logic
            if 'OTHER' in all_results:
                # If OTHER already exists from checkbox votes, don't double-count
                # The checkbox_responses already includes the properly weighted OTHER votes
                pass
            else:
                # If OTHER only exists from "other" responses, treat as single choice (full vote)
                all_results['OTHER'] = {'option_select': 'OTHER', 'count': other_count}
        
        # Convert to list and sort
        final_results = list(all_results.values())
        final_results.sort(key=lambda x: x['option_select'])
        
        return {
            "question_code": question_code,
            "results": final_results
        }
        
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        raise HTTPException(status_code=500, detail="Error fetching results")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
