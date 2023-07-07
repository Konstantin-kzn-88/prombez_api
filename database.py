from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Пример подключения к MySQL
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://u1082920_test_to:1501kZn1501!@server167.hosting.reg.ru/u1082920_fast_api_todo'

SQLALCHEMY_DATABASE_URL = 'sqlite:///./prom_bez.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
