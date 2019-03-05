# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from catalog_database_setup import Catalog, Base, CatalogItem, User
 
engine = create_engine('sqlite:///catalogitems.db')
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

#Items for Soccer
catalog1 = Catalog(user_id=1, name = "Soccer")

session.add(catalog1)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name = "Jersey", description = '''To soccer legend Diego Maradona of Argentina, "giving everything for the shirt" is a player's motto. In other words, the soccer jersey is everything a team stands for.
A brief overview of soccer jersey numbers and what they stand for is as follows:
	1.	Goalkeeper
	2.	Right back - defender
	3.	Defender's defender - center back
	4.	Lefty - defender or midfielder. The position historically gets its name from being positioned at the left side of the field.
	5.	In the US, it's the Center Half or Midfielder. In England, it's the Center Half or Defender.
	6.	Versatile position; In the US and Europe, it's the midfielder. In England, it's the Center Back. In Brazil, generally the Back, but all are versatile.
	7.	Attacker, usually right wing. In the US national team, it stands for Left Wing.
	8.	Two-way midfielder. The number represents a strong defense and offense player, or a dominant player.
	9.	Striker; goal-scorer. It's considered a very important number.
	10.	Dominant player who carries a lot of responsibilities on and off the field.
	11.	"Slasher". This is an attacker, such as a forward wing or wide midfielder; second most likely to score.''', catalog = catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name = "Soccer cleats", description = '''The soccer shoe has come a long way to say the least. Work boots are now high performance footwear that allows a soccer athlete to push his or her skills to limit. Designs today are not so much to protect players from injury as it is about maximizing their strategy. And as playing surfaces changed, in came soccer turf shoes. Makers designed lightweight shoes that allowed an athlete to kick with the side of the foot and lift the ball with the toe. And as long as designers throw in a little color and pizzazz, a player's look is complete. From cleats to lacing technology, makers accommodate the changing industry for the success of soccer athletes around the world, male and female alike.
The soccer shoe has undergone dramatic change to meet the growing demands of an ever-popular sport. Improved comfort, resiliency, grip, and even lacing and eyelet technology for a flatter, more comfortable fitting, are testament to how far the boot has come. Today soccer shoes allow more freedom to move, to score, and to entertain the spectator than ever before. ''', catalog = catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name = "Shinguards", description = '''A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury. These are commonly used in sports including association football, baseball, ice hockey, field hockey, lacrosse, cricket, mountain bike trials, and other sports.''', catalog = catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name = "Two shinguards", description = '''A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury. These are commonly used in sports including association football, baseball, ice hockey, field hockey, lacrosse, cricket, mountain bike trials, and other sports.''', catalog = catalog1)

session.add(catalogItem4)
session.commit()


#Items for basketBall
catalog2 = Catalog(user_id=1, name = "Basketball")

session.add(catalog2)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name = "Basketball hoop", description = '''horizontal circular metal hoop supporting a net through which players try to throw the basketball''', catalog = catalog2)

session.add(catalogItem1)
session.commit()



#Menu for Panda Garden
catalog3 = Catalog(user_id=1, name = "Baseball")

session.add(catalog3)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name = "Bat", description = '''A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches (7.0 cm) in diameter at the thickest part and no more than 42 inches (1.067 m) in length.''', catalog = catalog3)

session.add(catalogItem1)
session.commit()


#Items for Frisbee
catalog4 = Catalog(user_id=1, name = "Frisbee")

session.add(catalog4)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name = "Frisbee", description = '''A frisbee  is a gliding toy or sporting item that is generally plastic and roughly 8 to 10 inches (20 to 25 cm) in diameter with a pronounced lip. It is used recreationally and competitively for throwing and catching, as in flying disc games. The shape of the disc is an airfoil in cross-section which allows it to fly by generating lift as it moves through the air. Spinning it imparts a stabilizing gyroscopic force, allowing it to be both aimed and thrown for distance.''', catalog = catalog4)

session.add(catalogItem1)
session.commit()

#Items for Snowboarding
catalog5 = Catalog(user_id=1, name = "Snowboarding")

session.add(catalog5)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name = "Snowboard", description = '''All-mountain snowboards perform anywhere on a mountain-groomed runs, backcountry, even park and pipe. They may be directional (meaning downhill only) or twin-tip (for riding switch, meaning either direction).
Most boarders ride all-mountain boards. Because of their versatility, all-mountain boards are good for beginners who are still learning what terrain they like.''', catalog = catalog5)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name = "Goggles", description = '''Goggles are one of the most important pieces of equipment you can purchase; they are just as important as your jacket and pants. Any skier or snowboarder can tell you that not being able to see ruins a day as fast as poor fitting boots or a bad chili dog. All ski and snowboard goggles will offer some basic protection from wind and cold, but beyond the basics there are some key features to consider: lens type, lens color/tint, interchangeable lenses, frame size and fit.''', catalog = catalog5)

session.add(catalogItem1)
session.commit()

#Items for Rock Climbing
catalog6 = Catalog(user_id=1, name = "Rock Climbing")

session.add(catalog6)
session.commit()


#Items for Foosball
catalog7 = Catalog(user_id=1, name = "Foosball")

session.add(catalog7)
session.commit()


#Items for Skating
catalog8 = Catalog(user_id=1, name = "Skating")

session.add(catalog8)
session.commit()


#Items for Hockey
catalog9 = Catalog(user_id=1, name = "Hockey")

session.add(catalog9)
session.commit()



print "added catalog items!"