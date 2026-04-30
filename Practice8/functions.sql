CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name::VARCHAR, c.phone::VARCHAR
    FROM phonebook c
    WHERE c.first_name ILIKE '%' || p || '%'
       OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name::VARCHAR, p.phone::VARCHAR
    FROM phonebook p
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql; 