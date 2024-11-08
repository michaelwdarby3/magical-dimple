SELECT query, AVG(rating) as average_rating, COUNT(*) as feedback_count
FROM feedback
GROUP BY query
ORDER BY average_rating DESC;
