from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

# строка подключения
if config['fapi']['mode'] == "sqlite":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    SQLALCHEMY_ARGS = {"check_same_thread": False}
    print("Выбрана база данных SQLite")
elif config['fapi']['mode'] == "postgre":
    SQLALCHEMY_DATABASE_URL = URL.create(
        config['fapi']['psdriver'],
        username=config['fapi']['username'],
        password=config['fapi']['password'],
        host=config['fapi']['host'],
        port=config['fapi']['port'],
        database=config['fapi']['database']
    )
    SQLALCHEMY_ARGS = {}
    print("Выбрана база данных Postgre")

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=SQLALCHEMY_ARGS
)

# создаем сессию для работы с БД
SessionLocal = sessionmaker(autoflush=False, bind=engine)

#создаем базовый класс для моделей
Base = declarative_base()

# создаем модель, объекты которой будут храниться в бд
class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(128))
    submenus = relationship('Submenu', backref='submenu', lazy='dynamic',
                            cascade = "all, delete, delete-orphan" )

    def __repr__(self):
        return '<Menu id: {}, title: {}, description: {}>'.format(
            self.id,
            self.title,
            self.description
            )

class Submenu(Base):
    __tablename__ = "submenu"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(128))
    menu_id = Column(Integer, ForeignKey('menu.id'))
    dishes = relationship('Dish', backref='dish', lazy='dynamic',
                          cascade = "all, delete, delete-orphan" )

    def __repr__(self):
        return '<Submenu id: {}, title: {}, description: {}, menu_id: {}>'.format(
            self.id,
            self.title,
            self.description,
            self.menu_id
            )

class Dish(Base):
    __tablename__ = "dish"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(128))
    price = Column(Float)
    submenu_id = Column(Integer, ForeignKey('submenu.id'))

    def __repr__(self):
        return '<Dish id: {}, title: {}, description: {}, price: {}, submenu_id: {}>'.format(
            self.id,
            self.title,
            self.description,
            self.price,
            self.menu_id
            )

Base.metadata.create_all(bind=engine)
