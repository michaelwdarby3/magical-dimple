DELETE FROM feedback
WHERE created_at < NOW() - INTERVAL '%s days';
