-- init.sql

-- Create the 'users' table with fields matching users.csv
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    country VARCHAR(255)
);

-- Populate 'users' table with actual data from CSV file
COPY users(user_id, name, age, country)
FROM '/docker-entrypoint-initdb.d/users.csv'
DELIMITER ','
CSV HEADER;

-- Create the 'reviews' table
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate 'reviews' table with data from CSV
COPY reviews(review_id, user_id, review_text, product_name, product_type, created_at)
FROM '/docker-entrypoint-initdb.d/reviews.csv'
DELIMITER ','
CSV HEADER;


-- Indexes for faster searching on product_name and product_type
CREATE INDEX IF NOT EXISTS idx_reviews_product_name ON reviews (product_name);
CREATE INDEX IF NOT EXISTS idx_reviews_product_type ON reviews (product_type);

-- Index on user_id to improve joins and filtering in queries
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews (user_id);

-- Optionally, create an index on created_at for efficient date filtering (if needed)
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews (created_at);
