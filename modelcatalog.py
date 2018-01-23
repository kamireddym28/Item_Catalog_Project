from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SmartPhone, Base, PhoneModel, User

engine = create_engine('sqlite:///smartphonemodelcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')  # noqa
session.add(User1)
session.commit()

# Apple iPhone Modelcatalog
smartPhone1 = SmartPhone(user_id=1, name="Apple")

session.add(smartPhone1)
session.commit()

phoneModel1 = PhoneModel(name="iPhone X",
                         description="'DisplaySize: 5.8 inch',\
                         'CameraResolution: 12MP/7MP Back/Front',\
                         'RAM: 3 GB, Release: 11/2017'",
                         price="$999", os="ios 11.1.1",
                         memory="64 GB", smartPhone=smartPhone1,
                         user_id=1)

session.add(phoneModel1)
session.commit()

phoneModel2 = PhoneModel(name="iPhone 8",
                         description="'DisplaySize: 4.7 inch',\
                         'CameraResolution: 12MP/7MP Back/Front',\
                         'RAM: 2 GB, Release: 9/2017'",
                         price="$849", os="ios 11",
                         memory="256 GB", smartPhone=smartPhone1,
                         user_id=1)

session.add(phoneModel2)
session.commit()

phoneModel3 = PhoneModel(name="iPhone 7 Plus",
                         description="'DisplaySize: 5.5 inch',\
                         'CameraResolution: 12MP/7MP Back/Front', \
                         'RAM: 3 GB, Release: 9/2016'",
                         price="$769", os="ios 10.0.1",
                         memory="128 GB", smartPhone=smartPhone1,
                         user_id=1)

session.add(phoneModel3)
session.commit()

# Samsung Models
smartPhone2 = SmartPhone(user_id=1, name="Samsung")

session.add(smartPhone2)
session.commit()

phoneModel4 = PhoneModel(name="Galaxy S8",
                         description="'DisplaySize: 5.8 inch',\
                         'CameraResolution: 12MP/8MP Back/Front',\
                         'RAM: 4 GB, Release: 04/2017'",
                         price="$756", os="Android 7",
                         memory="64 GB", smartPhone=smartPhone2,
                         user_id=1)

session.add(phoneModel4)
session.commit()

phoneModel5 = PhoneModel(name="Galaxy S7 Edge",
                         description="'DisplaySize: 5.5 inch', \
                         'CameraResolution: 12MP/5MP Back/Front',\
                         'RAM: 4 GB, Release: 03/2016'",
                         price="$480.99", os="Android 6",
                         memory="32 GB", smartPhone=smartPhone2,
                         user_id=1)

session.add(phoneModel5)
session.commit()

phoneModel6 = PhoneModel(name="Galaxy Note 7",
                         description="'DisplaySize: 5.7 inch',\
                         'CameraResolution: 12MP/5MP Back/Front',\
                         'RAM: 4 GB, Release: 08/2016'",
                         price="$439", os="Android 6.0.1",
                         memory="64 GB", smartPhone=smartPhone2,
                         user_id=1)

session.add(phoneModel6)
session.commit()

# HTC Models
smartPhone3 = SmartPhone(user_id=1, name="HTC")

session.add(smartPhone3)
session.commit()

phoneModel7 = PhoneModel(name="HTC U11",
                         description="'DisplaySize: 5.5 inch', \
                         'CameraResolution: 12MP/16MP Back/Front',\
                         'RAM: 6 GB, Release: 05/2017'",
                         price="$649", os="Android 7.1",
                         memory="128 GB", smartPhone=smartPhone3,
                         user_id=1)

session.add(phoneModel7)
session.commit()

phoneModel8 = PhoneModel(name="HTC 10",
                         description="'DisplaySize: 5.2 inch',\
                         'CameraResolution: 12MP/5MP Back/Front',\
                         'RAM: 4 GB, Release: 05/2016'",
                         price="$359.99", os="Android 6.0.1",
                         memory="32 GB", smartPhone=smartPhone3,
                         user_id=1)

session.add(phoneModel8)
session.commit()

phoneModel9 = PhoneModel(name="HTC One M9",
                         description="'DisplaySize: 5 inch',\
                         'CameraResolution: 20MP/4MP Back/Front',\
                         'RAM: 3 GB, Release: 03/2015'",
                         price="$219.99", os="Android 6",
                         memory="32 GB", smartPhone=smartPhone3,
                         user_id=1)

session.add(phoneModel9)
session.commit()

# Google Models
smartPhone4 = SmartPhone(user_id=1, name="Google")

session.add(smartPhone4)
session.commit()

phoneModel10 = PhoneModel(name="Pixel 2 XL",
                          description="'DisplaySize: 6 inch', \
                          'CameraResolution: 12.2MP/8MP Back/Front',\
                          'RAM: 6 GB, Release: 10/2017'",
                          price="$949.99", os="Android 8",
                          memory="128 GB", smartPhone=smartPhone4,
                          user_id=1)

session.add(phoneModel10)
session.commit()

phoneModel11 = PhoneModel(name="Pixel 2",
                          description="'DisplaySize: 5 inch',\
                          'CameraResolution: 12.2MP/8MP Back/Front',\
                          'RAM: 4 GB, Release: 10/2017'",
                          price="$649.99", os="Android 8",
                          memory="64 GB", smartPhone=smartPhone4,
                          user_id=1)

session.add(phoneModel11)
session.commit()

phoneModel12 = PhoneModel(name="Pixel",
                          description="'DisplaySize: 5 inch', \
                          'CameraResolution: 12.3MP/8MP Back/Front',\
                          'RAM: 4 GB, Release: 10/2016'",
                          price="$549", os="Android 7.1",
                          memory="32 GB", smartPhone=smartPhone4,
                          user_id=1)

session.add(phoneModel12)
session.commit()

# Motorola Models
smartPhone5 = SmartPhone(user_id=1, name="Motorola")

session.add(smartPhone5)
session.commit()

phoneModel13 = PhoneModel(name="Moto X4",
                          description="'DisplaySize: 5.2 inch',\
                          'CameraResolution: 12MP/16MP Back/Front',\
                          'RAM: 3 GB, Release: 10/2017'",
                          price="$399.99", os="Android 7.1",
                          memory="32 GB", smartPhone=smartPhone5,
                          user_id=1)

session.add(phoneModel13)
session.commit()

phoneModel14 = PhoneModel(name="Moto G5 Plus",
                          description="'DisplaySize: 5.2 inch',\
                          'CameraResolution: 12MP/5MP Back/Front',\
                          'RAM: 4 GB, Release: 3/2017'",
                          price="$299.99", os="Android 7",
                          memory="64 GB", smartPhone=smartPhone5,
                          user_id=1)

session.add(phoneModel14)
session.commit()

phoneModel15 = PhoneModel(name="Moto E",
                          description="'DisplaySize: 4.5 inch',\
                          'CameraResolution: 5MP/0.3MP Back/VGA Front',\
                          'RAM: 1 GB, Release: 2/2015'",
                          price="$155.50", os="Android 5.1",
                          memory="8 GB", smartPhone=smartPhone5,
                          user_id=1)

session.add(phoneModel15)
session.commit()

# Microsoft Models
smartPhone6 = SmartPhone(user_id=1, name="Microsoft")

session.add(smartPhone6)
session.commit()

phoneModel16 = PhoneModel(name="Lumia 950 XL",
                          description="'DisplaySize: 5.7 inch',\
                          'CameraResolution: 20MP/5MP Back/Front',\
                          'RAM: 3 GB, Release: 11/2015'",
                          price="$449", os="Windows 10",
                          memory="32 GB", smartPhone=smartPhone6,
                          user_id=1)

session.add(phoneModel16)
session.commit()

phoneModel17 = PhoneModel(name="Lumia 640 XL",
                          description="'DisplaySize: 5.7 inch',\
                          'CameraResolution: 13MP/5MP Back/Front',\
                          'RAM: 1 GB, Release: 3/2015'",
                          price="$185.99", os="Windows 8.1",
                          memory="8 GB", smartPhone=smartPhone6,
                          user_id=1)

session.add(phoneModel17)
session.commit()

phoneModel18 = PhoneModel(name="Lumia 550",
                          description="'DisplaySize: 4.7 inch',\
                          'CameraResolution: 5MP/2MP Back/Front',\
                          'RAM: 1 GB, Release: 12/2015'",
                          price="$139", os="Windows 10",
                          memory="8 GB", smartPhone=smartPhone6,
                          user_id=1)

session.add(phoneModel18)
session.commit()

print "added smartphone catalog!"
