from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///pet_supplies.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class PetSupplies(Base):
    __tablename__ = 'Pet_Supplies'

    id = Column(Integer, primary_key=True)
    name = Column('Name', String)
    category = Column('Category', String)
    subcategory = Column('Sub category', String)
    image_url = Column('Image url', String)
    product_url = Column('Product url', String)
    rating = Column('Rating', Integer)
    num_ratings = Column('Num ratings', Integer)
    discount_price = Column('Discount price', Integer)
    regular_price = Column('Regular price', Integer)

    def __repr__(self):
        return f'Name: {self.name} Category: {self.category} Sub category: {self.subcategory} Image url: {self.image_url} Product url: {self.product_url} Rating: {self.rating} Num ratings: {self.num_ratings} Discount price: {self.discount_price} Regular price: {self.regular_price}'




