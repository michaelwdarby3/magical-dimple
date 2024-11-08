INSERT INTO feedback (query, response, rating, created_at)
VALUES (%s, %s, %s, NOW());
