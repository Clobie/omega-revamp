-- db_init.sql

-- Create a test table
CREATE TABLE IF NOT EXISTS test_entities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some placeholder test data
INSERT INTO test_entities (name, description) VALUES
    ('Entity Alpha', 'Description for test entity Alpha.'),
    ('Entity Beta', 'Description for test entity Beta.'),
    ('Entity Gamma', 'Description for test entity Gamma.');
