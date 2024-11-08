SELECT * FROM feedback
WHERE rating >= %s
ORDER BY created_at DESC;
