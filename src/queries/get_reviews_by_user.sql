SELECT * FROM reviews
WHERE user_id = %s
ORDER BY created_at DESC;
