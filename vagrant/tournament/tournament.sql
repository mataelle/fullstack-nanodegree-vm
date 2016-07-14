-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE player (
    id integer PRIMARY KEY,
    username varchar(40) NOT NULL
);

CREATE TABLE tournament (
    id integer PRIMARY KEY
);

CREATE TABLE round (
    id integer PRIMARY KEY,
    number integer NOT NULL,
    tournament integer references tournament(id)
);

CREATE TABLE match (
    id integer PRIMARY KEY,
    round integer references round(id),
    winner integer references player(id),
    loser integer references player(id)
);