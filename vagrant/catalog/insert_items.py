from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User


engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

autoUser = User(name = "anon", email = "anon@noreply.com")

category1 = Category(name = "Cooperative games")
category2 = Category(name = "Multiplayer games without elimination")

session.add(category1)
session.add(category2)
session.commit()

item1 = Item(name = "Arkham Horror",
             description = '''
                The game board is set in Lovecraft's fictional city of Arkham during 1926.
                Street, building and outdoor locations are featured, as well as otherworldly
                locations that investigators can venture into. Players each have an investigator,
                represented by a character card.''',
             category = category1, user=autoUser)

item2 = Item(name = "Arkham Horror",
             description = '''
                The game board is set in Lovecraft's fictional city of Arkham during 1926.
                Street, building and outdoor locations are featured, as well as otherworldly
                locations that investigators can venture into. Players each have an investigator,
                represented by a character card.''',
             category = category2, user=autoUser)

item3 = Item(name = "Pandemic",
             description = '''
                 The goal of Pandemic is for the players, in their randomly selected roles, to work
                 cooperatively to stop the spread of four diseases and cure them before
                 a pandemic occurs. Pandemic setup consists of a game board representing a network
                 connecting 48 cities on the map of the earth, two decks
                 of cards (Player cards and Infection cards),
                 four colors of cubes (each representing a different disease), six Research Stations,
                 and a pawn for each player. The Player cards include cards with each city
                 name (the same as those on the board); Special Event cards,
                 which can be played at specific times to take beneficial actions;
                 and Epidemic cards.
                 Infection cards consist of one card for each city on the board
                 and a color of the disease that will start there.''',
             category = category1, user=autoUser)

item4 = Item(name="Alias",
            description = '''
                Alias is a board game, where the objective of the players is to explain words
                to each other. Hence, Alias is similar to Taboo, but the only forbidden word
                in the explanations is the word to be explained. The game is played in teams
                of varying size, and fits well as a party game for larger crowds.
                The game is very competitive.''',
            category = category2, user=autoUser)

item5 = Item(name="Civilization",
            description = '''
                The Civilization board depicts areas around the Mediterranean Sea.
                The board is divided into many regions. Each player starts with
                a single population token, and attempts to grow and expand his
                empire over successive turns, trying to build the greatest civilization.''',
            category = category2, user=autoUser)

item6 = Item(name="Forbidden Island",
            description = '''
                Forbidden Island is a cooperative board game developed by Matt Leacock
                and published by Gamewright Games in 2010.[1] Two to four players take
                the roles of different adventurers, moving around a mysterious island,
                looking for hidden treasures as the island sinks around them. All players win
                if they find all the hidden treasures and they all make it back to the helicopter
                and fly away, and they all lose if they cannot.''',
            category = category1, user=autoUser)

session.add(item1)
session.add(item2)
session.add(item3)
session.add(item4)
session.add(item5)
session.add(item6)
session.commit()