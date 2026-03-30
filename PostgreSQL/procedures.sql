CREATE OR REPLACE PROCEDURE public.upsert_many_users(
    p_names TEXT[],
    p_surnames TEXT[],
    p_phones TEXT[],
    INOUT bad_data TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    bad_data := ARRAY[]::TEXT[];
    IF array_length(p_names, 1) != array_length(p_surnames, 1)
        OR array_length(p_names, 1) != array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^\+?[0-9]{11}$' THEN
            INSERT INTO phonebook(name, surname, phone)
            VALUES (p_names[i], p_surnames[i], p_phones[i])
            ON CONFLICT (name, surname)
            DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            bad_data := array_append(
                bad_data,
                p_names[i] || ' ' || p_surnames[i] || ' - ' || p_phones[i]
            );
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE public.delete_contact_proc(
    p_name TEXT DEFAULT NULL,
    p_surname TEXT DEFAULT NULL,
    p_phone TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM phonebook
        WHERE phone = p_phone;
    ELSE
        DELETE FROM phonebook
        WHERE name = p_name AND surname = p_surname;
    END IF;
END;
$$;