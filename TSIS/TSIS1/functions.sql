DROP FUNCTION IF EXISTS public.search_contacts(TEXT) CASCADE;
DROP FUNCTION IF EXISTS public.get_contacts_page(INT, INT) CASCADE;

CREATE FUNCTION public.search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INT,
    full_name TEXT,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE sql
AS $$
    SELECT
        c.id AS contact_id,
        c.name || ' ' || c.surname AS full_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(string_agg(p.phone || ' [' || p.type || ']', ', ' ORDER BY p.id), '') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id, c.name, c.surname, c.email, c.birthday, g.name
    HAVING
        c.name ILIKE '%' || p_query || '%'
        OR c.surname ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR COALESCE(string_agg(p.phone, ' '), '') ILIKE '%' || p_query || '%'
    ORDER BY c.name, c.surname;
$$;

CREATE FUNCTION public.get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE (
    contact_id INT,
    full_name TEXT,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE sql
AS $$
    SELECT
        c.id AS contact_id,
        c.name || ' ' || c.surname AS full_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(string_agg(p.phone || ' [' || p.type || ']', ', ' ORDER BY p.id), '') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id, c.name, c.surname, c.email, c.birthday, g.name
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
$$;
