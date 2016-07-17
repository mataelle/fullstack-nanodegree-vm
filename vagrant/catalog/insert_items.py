from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item


engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


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
             category = category1)

item2 = Item(name = "Arkham Horror",
             description = '''
                The game board is set in Lovecraft's fictional city of Arkham during 1926.
                Street, building and outdoor locations are featured, as well as otherworldly
                locations that investigators can venture into. Players each have an investigator,
                represented by a character card.''',
             category = category2)

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
             category = category1)
session.add(item1)
session.add(item2)
session.add(item3)
session.commit()