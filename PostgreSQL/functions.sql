CREATE OR REPLACE FUNCTION public.search_contacts(p_pattern TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE sql
AS $$
    SELECT phonebook.id, phonebook.name, phonebook.surname, phonebook.phone
    FROM phonebook
    WHERE phonebook.name ILIKE '%' || p_pattern || '%'
        OR phonebook.surname ILIKE '%' || p_pattern || '%'
        OR phonebook.phone LIKE '%' || p_pattern || '%'
    ORDER BY phonebook.id;
$$;


CREATE OR REPLACE FUNCTION public.get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE sql
AS $$
    SELECT phonebook.id, phonebook.name, phonebook.surname, phonebook.phone
    FROM phonebook
    ORDER BY phonebook.id
    LIMIT p_limit OFFSET p_offset;
$$;