SET SEARCH_PATH TO cv_pt, PUBLIC;

DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS workouts CASCADE;

CREATE TABLE users (
    id uuid PRIMARY KEY NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    height INT,
    weight INT
);

CREATE TABLE sessions (
    id uuid PRIMARY KEY NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL REFERENCES users(username),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    duration INTERVAL,
    volume INT
);

CREATE TABLE workouts (
    id uuid PRIMARY KEY NOT NULL UNIQUE,
    session_id uuid NOT NULL REFERENCES sessions(id),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    duration INTERVAL,
    reps INT,
    max_weight INT,
    volume INT
);

