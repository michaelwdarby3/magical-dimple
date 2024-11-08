SELECT user_id, COUNT(*) as review_count
FROM reviews
GROUP BY user_id
ORDER BY review_count DESC;
