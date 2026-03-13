-- HBnB initial seed data
-- Task 9: SQL Scripts for Table Generation and Initial Data

PRAGMA foreign_keys = ON;

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$A8oVwzE7J0C0sQ6f5b9fNehxJ4x7Jw0lM3m1Yg0XzV8QmQ2fQ6g3u',
    1
);

INSERT INTO amenities (id, name) VALUES
('7f4f0c4f-7d52-4d63-8e7d-4e5d6a9f1001', 'WiFi'),
('8a1d9b2c-2f4e-4f0a-9d44-91d6ef230002', 'Swimming Pool'),
('9c3e2f7d-5a61-43be-a2c1-6c8a8d440003', 'Air Conditioning');