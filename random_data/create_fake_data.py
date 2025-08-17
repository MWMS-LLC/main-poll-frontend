import psycopg2
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def create_fake_data():
    """Create fake users and voting data for testing"""
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres@localhost:5432/teen_poll')
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL database")
        
        # Create some fake users
        fake_users = []
        for i in range(10):
            user_uuid = f"fake-user-{i+1}"
            year_of_birth = random.randint(2007, 2012)
            
            cursor.execute("""
                INSERT INTO users (user_uuid, year_of_birth, created_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_uuid) DO NOTHING
            """, (user_uuid, year_of_birth, datetime.now()))
            
            fake_users.append(user_uuid)
        
        print(f"✅ Created {len(fake_users)} fake users")
        
        # Get some questions to vote on
        cursor.execute("SELECT question_code, question_text FROM questions LIMIT 5")
        questions = cursor.fetchall()
        
        print(f"✅ Found {len(questions)} questions to vote on")
        
        # Create fake votes for each question
        for question_code, question_text in questions:
            print(f"  📊 Creating votes for: {question_code}")
            
            # Get options for this question
            cursor.execute("SELECT option_select, option_text FROM options WHERE question_code = %s ORDER BY option_select", (question_code,))
            options = cursor.fetchall()
            
            if not options:
                continue
            
            # Create 5-15 votes per question
            num_votes = random.randint(5, 15)
            
            for i in range(num_votes):
                user_uuid = random.choice(fake_users)
                option_select, option_text = random.choice(options)
                
                # Randomly choose between single-choice and checkbox
                if random.random() < 0.7:  # 70% single-choice
                    # Single-choice vote
                    cursor.execute("""
                        INSERT INTO responses (
                            question_code, option_select, option_code, option_text, user_uuid,
                            question_text, question_number, category_name, category_id, block_number, created_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        question_code, option_select, f"OPT_{option_select}", option_text,
                        user_uuid, question_text, random.randint(1, 10), "Test Category", 1, 1, 
                        datetime.now() - timedelta(minutes=random.randint(1, 60))
                    ))
                else:
                    # Checkbox vote (select 1-3 options)
                    num_selected = random.randint(1, min(3, len(options)))
                    selected_options = random.sample(options, num_selected)
                    weight = 1.0 / num_selected
                    
                    for option_select, option_text in selected_options:
                        cursor.execute("""
                            INSERT INTO checkbox_responses (
                                question_code, option_select, option_code, option_text, user_uuid,
                                question_text, question_number, category_name, category_id, block_number, weight, created_at
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            question_code, option_select, f"OPT_{option_select}", option_text,
                            user_uuid, question_text, random.randint(1, 10), "Test Category", 1, 1, weight,
                            datetime.now() - timedelta(minutes=random.randint(1, 60))
                        ))
            
            print(f"    ✅ Created {num_votes} votes")
        
        # Create some "OTHER" responses
        for i in range(3):
            question_code, question_text = random.choice(questions)
            user_uuid = random.choice(fake_users)
            other_text = random.choice([
                "This is my personal opinion",
                "I think differently about this",
                "My experience is unique",
                "I have a different perspective",
                "This doesn't apply to me"
            ])
            
            cursor.execute("""
                INSERT INTO other_responses (
                    question_code, user_uuid, other_text, question_text, question_number,
                    category_name, category_id, block_number, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                question_code, user_uuid, other_text, question_text, random.randint(1, 10),
                "Test Category", 1, 1, datetime.now() - timedelta(minutes=random.randint(1, 60))
            ))
        
        print("    ✅ Created 3 OTHER responses")
        
        conn.commit()
        print("✅ All fake data created successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM responses")
        responses_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM checkbox_responses")
        checkbox_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM other_responses")
        other_count = cursor.fetchone()[0]
        
        print(f"\n📊 Fake Data Summary:")
        print(f"  Users: {users_count}")
        print(f"  Single-choice votes: {responses_count}")
        print(f"  Checkbox votes: {checkbox_count}")
        print(f"  Other responses: {other_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_fake_data()
