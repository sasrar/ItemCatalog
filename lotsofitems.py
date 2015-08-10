from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, User, Base

engine = create_engine('sqlite:///catalogItems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Items for Snowboarding
category1 = Category(user_id=1, name="Snowboarding")
session.add(category1)
session.commit()

item2 = Item(user_id=1, name="Snowboard", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     category=category1)
session.add(item2)
session.commit()


item1 = Item(user_id=1, name="Goggles", description="with garlic and parmesan",
                     category=category1)
session.add(item1)
session.commit()

# Items for Soccer
category2 = Category(user_id=1, name="Soccer")

session.add(category2)
session.commit()


item1 = Item(user_id=1, name="Ball", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     category=category2)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Cleats", description="A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook",
       category=category2)

session.add(item2)
session.commit()

print "added category items!"