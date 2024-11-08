INSERT INTO reviews (review_id, user_id, review_text, created_at)
VALUES (%s, %s, %s, NOW());
