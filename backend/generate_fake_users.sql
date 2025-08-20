-- 🎯 Generate 20 Fake Users with Random Responses
-- Run this in DBeaver connected to your Render database

-- First, let's see what columns are actually required by checking the table structure
-- Run this to see the table schemas:
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'responses' 
ORDER BY ordinal_position;

-- Then check the other tables:
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'checkbox_responses' 
ORDER BY ordinal_position;

SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'other_responses' 
ORDER BY ordinal_position;

-- For now, let's just create the users and see what we're working with:
INSERT INTO users (user_uuid, year_of_birth, created_at)
SELECT 
    gen_random_uuid() as user_uuid,
    (2007 + floor(random() * 6))::int as year_of_birth,  -- Random year 2007-2012
    (NOW() - (random() * 30 || ' days')::interval) as created_at  -- Random date within last 30 days
FROM generate_series(1, 20);

-- Show what was created:
SELECT 
    'Users Created' as metric,
    COUNT(*) as count
FROM users 
WHERE created_at >= NOW() - INTERVAL '1 day';
