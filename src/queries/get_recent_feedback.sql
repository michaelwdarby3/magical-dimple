SELECT * FROM feedback
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;
