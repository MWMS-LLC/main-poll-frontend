#!/usr/bin/env python3
"""
Import soundtracks from CSV to database
"""

import csv
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main_production import get_db_connection, execute_query

def clean_csv_value(value):
    """Clean CSV values and handle multi-line content"""
    if value is None:
        return None
    value = str(value).strip().replace('\ufeff', '')
    if '\n' in value:
        value = value.replace('\n', ' ')
    return value

def import_soundtracks():
    """Import soundtracks from CSV to database"""
    try:
        print("🎵 Starting soundtrack import...")
        
        # Read the CSV file
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'soundtracks.csv')
        
        if not os.path.exists(csv_path):
            print(f"❌ CSV file not found: {csv_path}")
            return False
        
        # Get database connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Clear existing soundtracks (optional - comment out if you want to keep existing)
                cursor.execute("DELETE FROM soundtracks")
                print("🗑️  Cleared existing soundtracks")
                
                # Import soundtracks
                print("📁 Importing soundtracks...")
                with open(csv_path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        # Map CSV columns to database columns
                        song_id = clean_csv_value(row['song_id'])
                        song_title = clean_csv_value(row['song_title'])
                        mood_tag = clean_csv_value(row['mood_tag'])
                        playlist_tag = clean_csv_value(row['playlist_tag'])
                        lyrics_snippet = clean_csv_value(row['lyrics_snippet'])
                        featured = row.get('featured', 'FALSE').upper() == 'TRUE'
                        featured_order = int(row.get('featured_order', 0)) if row.get('featured_order') and row.get('featured_order').strip() else 0
                        file_url = clean_csv_value(row['file_url'])
                        
                        # Insert soundtrack
                        cursor.execute("""
                            INSERT INTO soundtracks (
                                song_id, song_title, mood_tag, playlist_tag, lyrics_snippet, 
                                featured, featured_order, file_url, created_at
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (song_id) DO NOTHING
                        """, (
                            song_id, song_title, mood_tag, playlist_tag, lyrics_snippet,
                            featured, featured_order, file_url, datetime.now()
                        ))
                        
                        print(f"✅ Imported: {song_title}")
                
                # Commit all changes
                conn.commit()
                print("🎉 Soundtrack import completed successfully!")
                
                # Show summary
                cursor.execute("SELECT COUNT(*) as count FROM soundtracks")
                count = cursor.fetchone()[0]
                print(f"📊 Total soundtracks in database: {count}")
                
                return True
                
            except Exception as e:
                conn.rollback()
                print(f"❌ Error during import: {e}")
                return False
            finally:
                cursor.close()
                
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    success = import_soundtracks()
    if success:
        print("🎵 Soundtrack import completed!")
    else:
        print("❌ Soundtrack import failed!")
        sys.exit(1)

