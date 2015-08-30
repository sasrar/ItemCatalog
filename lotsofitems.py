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

# Items for Snowboarding Category
category1 = Category(user_id=1, name="Snowboarding")
session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Snowboard", description="a board resembling a short, broad ski, used for sliding downhill on snow",
                     category=category1)
session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Goggles", description="close-fitting eyeglasses with side shields, for protecting the eyes from glare, dust, water, etc",
                     category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Helmet", description="a hard protective hat for snowy conditions",
                     category=category1)
session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Boots", description="a sturdy item of footwear covering the foot",
                     category=category1)
session.add(item4)
session.commit()

# Items for Soccer Category
category2 = Category(user_id=1, name="Soccer")
session.add(category2)
session.commit()


item1 = Item(user_id=1, name="Soccer Ball", description="a solid or hollow sphere or ovoid, especially one that is kicked, thrown, or hit in a game",
                     category=category2)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Soccer Cleats", description="athletic shoes with a cleated sole",
       category=category2)
session.add(item2)
session.commit()

# Items for Baseball Category
category3 = Category(user_id=1, name="Baseball")
session.add(category3)
session.commit()

item1 = Item(user_id=1, name="Baseball", description="the hard ball used in the game of baseball",
            	category=category3)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Cleats", description="athletic shoes with a cleated sole, typically used when playing football",
       			category=category3)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Baseball Gloves", description="a large leather glove worn by baseball players of the defending team which assist players in catching and fielding balls",
       			category=category3)
session.add(item3)
session.commit()

# Items for Basketball Category
category4 = Category(user_id=1, name="Basketball")
session.add(category4)
session.commit()

item1 = Item(user_id=1, name="Basketball", description="the inflated ball used in the game of basketball",
            	category=category4)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Basketball Shoes", description="athletic shoes used when playing basketball",
       			category=category4)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Basketball Hoop", description="horizontal circular metal hoop supporting a net through which players try to throw the basketball",
       			category=category4)
session.add(item3)
session.commit()

print "added category items!"