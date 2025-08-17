from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pg8000
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Teen Poll API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you might want to restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function - PRODUCTION ONLY
def get_db_connection():
    """Get database connection to Render database"""
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.error("DATABASE_URL environment variable is not set!")
            return None
        
        # Parse DATABASE_URL to get connection parameters
        # Format: postgresql://username:password@host:port/database
        try:
            logger.info(f"Connecting to production database...")
            
            # Remove postgresql:// prefix
            url_without_prefix = database_url.replace("postgresql://", "")
            
            # Split user:pass@host:port/database
            user_pass_part, host_port_db = url_without_prefix.split("@", 1)
            user, password = user_pass_part.split(":", 1)
            host_port, database = host_port_db.split("/", 1)
            host, port = host_port.split(":", 1)
            port = int(port)
            
            logger.info(f"Production connection: host={host}, port={port}, database={database}, user={user}")
        except Exception as e:
            logger.error(f"Failed to parse DATABASE_URL: {e}")
            return None
        
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

@app.get("/health")
async def health():
    """Health check endpoint that doesn't require database"""
    return {"status": "healthy", "timestamp": str(datetime.now())}

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
        # Validate user data
        if not isinstance(user.get('user_uuid'), str):
            raise HTTPException(status_code=400, detail="user_uuid must be a string")
        if not isinstance(user.get('year_of_birth'), int):
            raise HTTPException(status_code=400, detail="year_of_birth must be an integer")
        
        # Validate age (2007-2012)
        if user['year_of_birth'] < 2007 or user['year_of_birth'] > 2012:
            raise HTTPException(status_code=400, detail="Invalid year of birth. Must be between 2007-2012.")
        
        query = """
            INSERT INTO users (user_uuid, year_of_birth, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_uuid) DO NOTHING
        """
        execute_query(query, (user['user_uuid'], user['year_of_birth'], datetime.now()), fetch=False)
        return {"message": "User created successfully", "user_uuid": user['user_uuid']}
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
        
        # Validate vote data
        if not isinstance(vote_data.get('question_code'), str):
            raise HTTPException(status_code=400, detail="question_code must be a string")
        if not isinstance(vote_data.get('option_select'), str):
            raise HTTPException(status_code=400, detail="option_select must be a string")
        if not isinstance(vote_data.get('user_uuid'), str):
            raise HTTPException(status_code=400, detail="user_uuid must be a string")
        
        # Get question and category details for denormalization
        question_query = """
            SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            WHERE q.question_code = %s
        """
        question_results = execute_query(question_query, (vote_data['question_code'],))
        
        if not question_results:
            raise HTTPException(status_code=400, detail="Question not found")
        
        question_info = question_results[0]
        
        # Insert the vote
        vote_query = """
            INSERT INTO responses (question_code, option_select, user_uuid, question_text, question_number, 
                                 category_name, category_id, block_number, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(vote_query, (
            vote_data['question_code'],
            vote_data['option_select'],
            vote_data['user_uuid'],
            question_info['question_text'],
            question_info['question_number'],
            question_info['category_name'],
            question_info['category_id'],
            question_info['block_number'],
            datetime.now()
        ), fetch=False)
        
        return {"message": "Vote recorded successfully"}
        
    except Exception as e:
        logger.error(f"Vote recording failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to record vote")

@app.post("/api/checkbox_vote")
async def checkbox_vote(vote_data: Dict[str, Any]):
    """Record a checkbox vote with multiple selections"""
    try:
        logger.info(f"Received checkbox vote request: {vote_data}")
        
        # Validate vote data
        if not isinstance(vote_data.get('question_code'), str):
            raise HTTPException(status_code=400, detail="question_code must be a string")
        if not isinstance(vote_data.get('selected_options'), list):
            raise HTTPException(status_code=400, detail="selected_options must be a list")
        if not isinstance(vote_data.get('user_uuid'), str):
            raise HTTPException(status_code=400, detail="user_uuid must be a string")
        
        # Get question and category details
        question_query = """
            SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            WHERE q.question_code = %s
        """
        question_results = execute_query(question_query, (vote_data['question_code'],))
        
        if not question_results:
            raise HTTPException(status_code=400, detail="Question not found")
        
        question_info = question_results[0]
        
        # Calculate weight for each option (equal distribution)
        total_options = len(vote_data['selected_options'])
        weight = 1.0 / total_options if total_options > 0 else 0
        
        # Insert each selected option
        for option in vote_data['selected_options']:
            if option == "OTHER":
                # Handle "OTHER" option - record in other_responses
                other_query = """
                    INSERT INTO other_responses (question_code, user_uuid, question_text, question_number,
                                               category_name, category_id, block_number, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_query(other_query, (
                    vote_data['question_code'],
                    vote_data['user_uuid'],
                    question_info['question_text'],
                    question_info['question_number'],
                    question_info['category_name'],
                    question_info['category_id'],
                    question_info['block_number'],
                    datetime.now()
                ), fetch=False)
            else:
                # Record in checkbox_responses with calculated weight
                checkbox_query = """
                    INSERT INTO checkbox_responses (question_code, option_select, user_uuid, weight,
                                                  question_text, question_number, category_name, category_id, block_number, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_query(checkbox_query, (
                    vote_data['question_code'],
                    option,
                    vote_data['user_uuid'],
                    weight,
                    question_info['question_text'],
                    question_info['question_number'],
                    question_info['category_name'],
                    question_info['category_id'],
                    question_info['block_number'],
                    datetime.now()
                ), fetch=False)
        
        return {"message": "Checkbox vote recorded successfully"}
        
    except Exception as e:
        logger.error(f"Checkbox vote recording failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to record checkbox vote")

@app.get("/api/results/{question_code}")
async def get_results(question_code: str):
    """Get results for a specific question"""
    try:
        # Get question details
        question_query = "SELECT * FROM questions WHERE question_code = %s"
        question_results = execute_query(question_query, (question_code,))
        
        if not question_results:
            raise HTTPException(status_code=404, detail="Question not found")
        
        question = question_results[0]
        
        if question['question_type'] == 'checkbox':
            # For checkbox questions, get results from checkbox_responses
            results_query = """
                SELECT option_select, COUNT(*) as count, SUM(weight) as total_weight
                FROM checkbox_responses 
                WHERE question_code = %s 
                GROUP BY option_select
                ORDER BY total_weight DESC
            """
            results = execute_query(results_query, (question_code,))
            
            # Calculate total responses
            total_responses = sum(result['total_weight'] for result in results)
            
            # Format results
            formatted_results = []
            for result in results:
                percentage = (result['total_weight'] / total_responses * 100) if total_responses > 0 else 0
                formatted_results.append({
                    "option": result['option_select'],
                    "count": result['total_weight'],
                    "percentage": round(percentage, 1)
                })
            
            return {
                "question_code": question_code,
                "question_text": question['question_text'],
                "question_type": "checkbox",
                "results": formatted_results,
                "total_responses": total_responses
            }
            
        else:
            # For single-choice questions, get results from responses
            results_query = """
                SELECT option_select, COUNT(*) as count
                FROM responses 
                WHERE question_code = %s 
                GROUP BY option_select
                ORDER BY count DESC
            """
            results = execute_query(results_query, (question_code,))
            
            # Calculate total responses
            total_responses = sum(result['count'] for result in results)
            
            # Format results
            formatted_results = []
            for result in results:
                percentage = (result['count'] / total_responses * 100) if total_responses > 0 else 0
                formatted_results.append({
                    "option": result['option_select'],
                    "count": result['count'],
                    "percentage": round(percentage, 1)
                })
            
            return {
                "question_code": question_code,
                "question_text": question['question_text'],
                "question_type": "single_choice",
                "results": formatted_results,
                "total_responses": total_responses
            }
            
    except Exception as e:
        logger.error(f"Failed to get results: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve results")

@app.get("/api/soundtracks")
async def get_soundtracks():
    """Get all soundtracks"""
    try:
        query = "SELECT * FROM soundtracks ORDER BY id"
        results = execute_query(query)
        logger.info(f"Retrieved {len(results)} soundtracks")
        return results
    except Exception as e:
        logger.error(f"Error retrieving soundtracks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve soundtracks: {e}")

@app.get("/api/soundtracks/playlists")
async def get_playlists():
    """Get all unique playlists"""
    try:
        query = "SELECT DISTINCT playlist_tag FROM soundtracks WHERE playlist_tag IS NOT NULL ORDER BY playlist_tag"
        results = execute_query(query)
        playlists = [result['playlist_tag'] for result in results]
        logger.info(f"Retrieved {len(playlists)} playlists")
        return playlists
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve playlists: {e}")

@app.get("/test")
async def test():
    """Test endpoint for debugging"""
    return {"message": "Backend is running!", "timestamp": str(datetime.now())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
