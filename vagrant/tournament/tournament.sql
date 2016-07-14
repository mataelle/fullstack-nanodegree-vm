-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE if exists player cascade;
DROP TABLE if exists match;

CREATE TABLE player (
    id serial PRIMARY KEY,
    username varchar(40) NOT NULL
);

CREATE TABLE match (
    id serial PRIMARY KEY,
    winner integer references player(id),
    loser integer references player(id)
);