SET SEARCH_PATH TO cv_pt, PUBLIC;

CREATE OR REPLACE FUNCTION create_user(
    _id UUID,
    _username VARCHAR(255),
    _password VARCHAR(255)
) RETURNS VOID AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM cv_pt.public.users WHERE username = _username) THEN
        RAISE EXCEPTION 'Username already exists';
    ELSE
        INSERT INTO cv_pt.public.users (id, username, password)
        VALUES (_id, _username, _password);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_session(
    _id uuid,
    _username VARCHAR(255),
    _created_at TIMESTAMP,
    _duration INTERVAL,
    _volume INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO cv_pt.public.sessions (id, username, created_at, duration, volume)
    VALUES (_id, _username, _created_at, _duration, _volume);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_workout(
    _id uuid,
    _session_id uuid,
    _name VARCHAR(255),
    _created_at TIMESTAMP,
    _duration INTERVAL,
    _reps INT,
    _weight INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO cv_pt.public.workouts (id, session_id, name, created_at, duration, reps, weight)
    VALUES (_id, _session_id, _name, _created_at, _duration, _reps, _weight);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_user(
    _username VARCHAR(255)
) RETURNS BOOLEAN AS $$
BEGIN
    PERFORM username FROM cv_pt.public.users WHERE username = _username;
    IF FOUND THEN
        RETURN TRUE;
    END IF;
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_password(
    _username VARCHAR(255),
    _password VARCHAR(255)
) RETURNS BOOLEAN AS $$
BEGIN
    PERFORM username FROM cv_pt.public.users WHERE username = _username AND password = _password;
    IF FOUND THEN
        RETURN TRUE;
    END IF;
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_user_session(
    _username VARCHAR(255),
    _session_token VARCHAR(255)
) RETURNS VOID AS $$
BEGIN
    INSERT INTO cv_pt.public.user_sessions (user_id, session_token)
    VALUES ((SELECT id FROM cv_pt.public.users WHERE username = _username), _session_token);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_user_session(
    _session_token VARCHAR(255)
) RETURNS VOID AS $$
BEGIN
    DELETE FROM cv_pt.public.user_sessions WHERE session_token = _session_token;
END;
$$ LANGUAGE plpgsql;