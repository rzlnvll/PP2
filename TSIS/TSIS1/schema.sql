-- Clean reset for extended phonebook project
DROP FUNCTION IF EXISTS public.search_contacts(TEXT) CASCADE;
DROP FUNCTION IF EXISTS public.get_contacts_page(INT, INT) CASCADE;

DROP PROCEDURE IF EXISTS public.add_phone(VARCHAR, VARCHAR, VARCHAR) CASCADE;
DROP PROCEDURE IF EXISTS public.add_phone(TEXT, TEXT, TEXT) CASCADE;
DROP PROCEDURE IF EXISTS public.move_to_group(VARCHAR, VARCHAR) CASCADE;
DROP PROCEDURE IF EXISTS public.move_to_group(TEXT, TEXT) CASCADE;

DROP TABLE IF EXISTS phones CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS phonebook CASCADE;

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, surname)
);

CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE(contact_id, phone)
);

INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;
