import sqlite3
import uuid
from datetime import datetime

def add_fake_data():
    """Add fake data to responses and checkbox_responses tables for testing"""
    
    # Connect to database
    conn = sqlite3.connect('teenpoll.db')
    cursor = conn.cursor()
    
    try:
        # Generate a fake user_uuid
        fake_user_uuid = str(uuid.uuid4())
        
        # Add fake user
        cursor.execute("""
            INSERT INTO users (user_uuid, year_of_birth, created_at)
            VALUES (?, ?, ?)
        """, (fake_user_uuid, 2008, datetime.now().isoformat()))
        
        print(f"✅ Added fake user: {fake_user_uuid}")
        
        # Add fake single-choice votes to responses table
        fake_responses = [
            ('1_1', 'A', 1, 'A', 'Unpaired. Unbothered. Still in orbit.', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'B', 2, 'B', 'Pairing mode on. Still blinking ...', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'A', 1, 'A', 'Unpaired. Unbothered. Still in orbit.', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'C', 3, 'C', 'Connected. Kinda laggy. But we\'re updating.', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'A', 1, 'A', 'Unpaired. Unbothered. Still in orbit.', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'D', 4, 'D', 'Patch notes dropping soon. Heart.exe rebooting.', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'B', 2, 'B', 'Pairing mode on. Still blinking ...', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
            ('1_1', 'A', 1, 'A', 'Unpaired. Unbothered. Still in orbit.', fake_user_uuid, 'What is your love life status?', 'Love Life', 1, 1, datetime.now().isoformat()),
        ]
        
        cursor.executemany("""
            INSERT INTO responses (question_code, option_select, option_id, option_code, option_text, user_uuid, question_text, category_name, category_id, block_number, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, fake_responses)
        
        print(f"✅ Added {len(fake_responses)} fake single-choice votes")
        
        # Add fake checkbox votes to checkbox_responses table
        fake_checkbox_responses = [
            ('1_4', 'A', 1, 'A', 'Kindness and empathy', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 1.0, datetime.now().isoformat()),
            ('1_4', 'B', 2, 'B', 'Sense of humor', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 0.5, datetime.now().isoformat()),
            ('1_4', 'A', 1, 'A', 'Kindness and empathy', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 1.0, datetime.now().isoformat()),
            ('1_4', 'C', 3, 'C', 'Intelligence', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 0.33, datetime.now().isoformat()),
            ('1_4', 'D', 4, 'D', 'Physical attraction', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 0.33, datetime.now().isoformat()),
            ('1_4', 'A', 1, 'A', 'Kindness and empathy', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 0.33, datetime.now().isoformat()),
            ('1_4', 'B', 2, 'B', 'Sense of humor', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 0.5, datetime.now().isoformat()),
            ('1_4', 'C', 3, 'C', 'Intelligence', fake_user_uuid, 'What do you look for in a partner?', 'Love Life', 1, 1, 0.5, datetime.now().isoformat()),
        ]
        
        cursor.executemany("""
            INSERT INTO checkbox_responses (question_code, option_select, option_id, option_code, option_text, user_uuid, question_text, category_name, category_id, block_number, weight, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, fake_checkbox_responses)
        
        print(f"✅ Added {len(fake_checkbox_responses)} fake checkbox votes")
        
        # Commit the changes
        conn.commit()
        print("✅ All fake data added successfully!")
        
        # Show the results
        print("\n📊 Current vote counts:")
        
        # Single choice results
        cursor.execute("""
            SELECT option_select, COUNT(*) as count 
            FROM responses 
            WHERE question_code = '1_1' 
            GROUP BY option_select
        """)
        single_results = cursor.fetchall()
        print("Single choice (1_1):")
        for option, count in single_results:
            print(f"  {option}: {count} votes")
        
        # Checkbox results
        cursor.execute("""
            SELECT option_select, SUM(weight) as total_weight 
            FROM checkbox_responses 
            WHERE question_code = '1_4' 
            GROUP BY option_select
        """)
        checkbox_results = cursor.fetchall()
        print("Checkbox (1_4):")
        for option, weight in checkbox_results:
            print(f"  {option}: {weight:.2f} weighted votes")
        
    except Exception as e:
        print(f"❌ Error adding fake data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_fake_data()
