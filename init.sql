-- init.sql

-- Create the 'users' table with fields matching users.csv
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    country VARCHAR(255)
);

-- Populate 'users' table with actual data from CSV file
COPY users(user_id, name, age, country)
FROM '/docker-entrypoint-initdb.d/users.csv'
DELIMITER ','
CSV HEADER;

-- Create the 'reviews' table with fields matching reviews.csv
CREATE TABLE IF NOT EXISTS reviews (
    review_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    created_at TIMESTAMP
);

-- Populate 'reviews' table with actual data from CSV file
COPY reviews(review_id, user_id, review_text, created_at)
FROM '/docker-entrypoint-initdb.d/reviews.csv'
DELIMITER ','
CSV HEADER;
