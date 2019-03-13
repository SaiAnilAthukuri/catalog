from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from mobile_setup import *

engine = create_engine('sqlite:///mobiles.db')
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

# Delete MobilesCompanyName if exisitng.
session.query(MobileCompanyName).delete()
# Delete MobileName if exisitng.
session.query(MobileName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(
    name="Athukuri Sai Anil",
    email="saianilathukuri2016@gmail.com")
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample Mobile companys
Company1 = MobileCompanyName(
    name="Oppo",
    user_id=1)
session.add(Company1)
session.commit()

Company2 = MobileCompanyName(
    name="Vivo",
    user_id=1)
session.add(Company2)
session.commit

Company3 = MobileCompanyName(
    name="HTC",
    user_id=1)
session.add(Company3)
session.commit()

Company4 = MobileCompanyName(
    name="Honor",
    user_id=1)
session.add(Company4)
session.commit()

Company5 = MobileCompanyName(
    name="Mi",
    user_id=1)
session.add(Company5)
session.commit()
print (" Add Mobile Compary Name")

# Populare a mobiles with models for testing
# Using different users for mobiles names year also
Name1 = MobileName(
    modelname="Oppo k1",
    processor="Snapdragon 660",
    ram="4GB",
    rom="64GB",
    price="17,000",
    screensize="6.4",
    rating="Very good",
    date=datetime.datetime.now(),
    mobilecompanynameid=1,
    user_id=1)
session.add(Name1)
session.commit()

Name2 = MobileName(
    modelname="Oppo R15 pro",
    processor="Snapdragon 660",
    ram="6GB",
    rom="128GB",
    price="25,000",
    screensize="6.28",
    rating="Very good",
    date=datetime.datetime.now(),
    mobilecompanynameid=1,
    user_id=1)
session.add(Name2)
session.commit()

Name3 = MobileName(
    modelname="Vivo v9 pro",
    processor="Snapdragon 660",
    ram="6GB",
    rom="64GB",
    price="15,000",
    screensize="6.3",
    rating="good",
    date=datetime.datetime.now(),
    mobilecompanynameid=2,
    user_id=1)
session.add(Name3)
session.commit()

Name4 = MobileName(
    modelname="Honor 10 lite",
    processor="Kirin 710",
    ram="4GB",
    rom="64GB",
    price="14,000",
    screensize="6.21",
    rating="Very good",
    date=datetime.datetime.now(),
    mobilecompanynameid=4,
    user_id=1)
session.add(Name4)
session.commit()

Name5 = MobileName(
    modelname="Note 5 pro",
    processor="Snapdragon 636",
    ram="4GB",
    rom="64GB",
    price="13,000",
    screensize="6.0",
    rating="Very good",
    date=datetime.datetime.now(),
    mobilecompanynameid=5,
    user_id=1)
session.add(Name5)
session.commit()

Name6 = MobileName(
    modelname="Note 6 Pro",
    processor="Snapdragon 660",
    ram="4GB",
    rom="64GB",
    price="15,000",
    screensize="6.26",
    rating="good",
    date=datetime.datetime.now(),
    mobilecompanynameid=5,
    user_id=1)
session.add(Name6)
session.commit()

print("Your mobiles database has been inserted!")
