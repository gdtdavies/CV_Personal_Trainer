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

CREATE OR REPLACE FUNCTION start_session(
    _session_token uuid,
    _username VARCHAR(255)
) RETURNS VOID AS $$
BEGIN
    INSERT INTO cv_pt.public.sessions (id, username) VALUES (_session_token, _username);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION end_session(
    _session_token uuid,
    _duration INTERVAL,
    _volume INT
) RETURNS VOID AS $$
BEGIN
    UPDATE cv_pt.public.sessions
    SET duration = _duration, volume = _volume
    WHERE id = _session_token;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_session_duration(
    _session_token uuid
) RETURNS INTERVAL AS $$
BEGIN
    RETURN (SELECT NOW() - created_at FROM cv_pt.public.sessions WHERE id = _session_token);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION start_workout(
    _workout_id uuid,
    _session_id uuid,
    _name VARCHAR(255)
) RETURNS VOID AS $$
BEGIN
    INSERT INTO cv_pt.public.workouts (id, session_id, name)
    VALUES (_workout_id, _session_id, _name);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION end_workout(
    _workout_id uuid,
    _reps INT,
    _weight INT,
    _volume INT
) RETURNS VOID AS $$
BEGIN
    UPDATE cv_pt.public.workouts
    SET duration = (NOW() - created_at), reps = _reps, max_weight = _weight, volume = _volume
    WHERE id = _workout_id;
END;
$$ LANGUAGE plpgsql;