import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    def __str__(self):
        return f'Book {self.id}: ({self.title}, {self.publisher_id})'
    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Shop {self.id}: {self.name}'

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'Stock {self.id}: {self.book_id}, {self.shop_id}, {self.count}'
class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'Sale {self.id}: {self.stock_id}, {self.date_sale}, {self.price}, {self.count}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = "postgresql://postgres:arkadysql@localhost:5432/netology_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
publisher1 = Publisher(name='Arkady Podkolzin')
publisher2 = Publisher(name='Anastasia Birykova')
book1 = Book(title='Любовь', publisher_id=1)
book2 = Book(title='Страсть', publisher_id=2)
shop1 = Shop(name='Читай-город')
shop2 = Shop(name='Книжный')
stock1 = Stock(book_id=1, shop_id=1, count=10)
stock2 = Stock(book_id=2, shop_id=2, count=15)
sale1 = Sale(stock_id=1, date_sale='26.04.2023', price=15000, count=1)
sale2 = Sale(stock_id=2, date_sale='20.03.2023', price=20000, count=2)
session.add(publisher1)
session.add(publisher2)
session.add(book1)
session.add(book2)
session.add(shop1)
session.add(shop2)
session.add(stock1)
session.add(stock2)
session.add(sale1)
session.add(sale2)
session.commit()
qr = session.query(Book, Shop, Sale, Publisher).join(Book).join(Stock).join(Sale).join(Shop)
publisher_name = input('Имя издателя: ')
publisher_id = int(input('Идентификатор издателя: '))
def get_info(publisher_name=None, publisher_id=None):
    if publisher_id == 0:
        for c in qr.filter(Publisher.name==publisher_name).all():
            print(f'{c.Book.title}|{c.Shop.name}|{c.Sale.price}|{c.Sale.date_sale}')
    elif publisher_id != 0:
        for c in qr.filter(Publisher.id == publisher_id).all():
            print(f'{c.Book.title}|{c.Shop.name}|{c.Sale.price}|{c.Sale.date_sale}')
get_info(publisher_name, publisher_id)
session.close()