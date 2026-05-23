DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE url_checks (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url_id bigint REFERENCES urls(id) ON DELETE CASCADE NOT NULL,
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
);
