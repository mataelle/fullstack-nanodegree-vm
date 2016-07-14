#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('delete from match *;')
    conn.commit()
    cur.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('delete from player *;')
    cur.execute('delete from match *;')
    conn.commit()
    cur.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from player;')
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into player (username) values (%s);", (name,))
    conn.commit()
    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    query = '''
    select a.id, a.name, b.wins, a.matches from
        (select p.id as id, p.username as name, count(m.winner) as matches
            from player as p left join match as m on p.id = m.winner or p.id = m.loser group by p.id)
        as a join
        (select p.id as id, count(m.winner) as wins
            from player as p left join match as m on p.id = m.winner group by p.id)
        as b
        on a.id=b.id order by b.wins;
    '''

    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('insert into match (winner, loser) values (%s, %s);',
                (winner, loser))
    conn.commit()
    cur.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = '''
        WITH new_table as (
        select p.id as id, p.username as name, count(m.winner) as wins, ROW_NUMBER() OVER(ORDER BY count(m.winner)) AS RowNumber
            from player as p left join match as m on p.id = m.winner
            group by p.id
            order by wins
        )
        select a.id as id1, a.name as name1, b.id as id2, b.name as name2 from
            new_table as a, new_table as b
            where a.RowNumber%2 != b.RowNumber%2 and
                 (a.RowNumber-1)/2 = (b.RowNumber-1)/2 and
                  a.id < b.id;

    '''

    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows