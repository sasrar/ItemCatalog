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
                     image="http://store.bobos.com/images/product/r/ride-youth-lil-buck-snowboard-(2014)-256px-256px.png",
                     category=category1)
session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Goggles", description="close-fitting eyeglasses with side shields, for protecting the eyes from glare, dust, water, etc",
                     image="https://images-na.ssl-images-amazon.com/images/I/61BdsTJgJfL._SL256_.jpg",
                     category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Helmet", description="a hard protective hat for snowy conditions",
                     image="http://www.trespass.com/media/catalog/product/cache/1/small_image/256x/9df78eab33525d08d6e5fb8d27136e95/f/u/furillo_black.jpg",
                     category=category1)
session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Boots", description="a sturdy item of footwear covering the foot",
                     image="http://static.wixstatic.com/media/f6495c_51e51a35457541a1aef4acdce568543d.jpg_256",
                     category=category1)
session.add(item4)
session.commit()

# Items for Soccer Category
category2 = Category(user_id=1, name="Soccer")
session.add(category2)
session.commit()


item1 = Item(user_id=1, name="Soccer Ball", description="a solid or hollow sphere or ovoid, especially one that is kicked, thrown, or hit in a game",
                     image="http://kindersay.com/files/images/soccer-ball.png",
                     category=category2)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Soccer Cleats", description="athletic shoes with a cleated sole",
              image="http://images.bwbx.io/cms/2014-07-16/0716_soccer_cleats_970-630x420.jpg",
              category=category2)
session.add(item2)
session.commit()

# Items for Baseball Category
category3 = Category(user_id=1, name="Baseball")
session.add(category3)
session.commit()

item1 = Item(user_id=1, name="Baseball", description="the hard ball used in the game of baseball",
            	image="http://vignette3.wikia.nocookie.net/pawnstarsthegame/images/d/d1/Baseball_Signed_By_1951_Yankees.png/revision/latest?cb=20111222123052",
              category=category3)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Cleats", description="athletic shoes with a cleated sole, typically used when playing football",
            image="http://wac.aee8.edgecastcdn.net/80AEE8/p/p/productphotos/4777-1_display.jpg",
            category=category3)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Baseball Gloves", description="a large leather glove worn by baseball players of the defending team which assist players in catching and fielding balls",
            image="http://i5.walmartimages.com/dfw/dce07b8c-973c/k2-_d4deba69-e424-49ef-be28-d026faba1763.v1.jpg",
            category=category3)
session.add(item3)
session.commit()

# Items for Basketball Category
category4 = Category(user_id=1, name="Basketball")
session.add(category4)
session.commit()

item1 = Item(user_id=1, name="Basketball", description="the inflated ball used in the game of basketball",
            image="http://www.prepcasts.com/wp-content/uploads/2014/04/BasketballStockImage.jpg",
            category=category4)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Basketball Shoes", description="athletic shoes used when playing basketball",
            image="http://cconnect.s3.amazonaws.com/wp-content/uploads/2014/01/Nike-Kobe-9-Elite-All-Star-Basketball-Shoe-large.jpg",
            category=category4)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Basketball Hoop", description="horizontal circular metal hoop supporting a net through which players try to throw the basketball",
            image="http://images.vectorhq.com/images/previews/c6e/basketball-hoop-psd-452366.png",
            category=category4)
session.add(item3)
session.commit()

print "added category items!"