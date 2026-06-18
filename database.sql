DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    created_at timestamp NOT NULL
);
