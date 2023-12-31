import models
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

if __name__ == '__main__':

    # строка подключения
    sqlite_database = "sqlite:///prom_bez.db"
    # создаем движок SqlAlchemy
    engine = create_engine(sqlite_database, echo=True)

    # создаем сессию подключения к бд
    with Session(autoflush=False, bind=engine) as db:
        records = db.query(models.Organization, models.Object).filter(models.Organization.user_id == 3).filter(models.Object.org_id == 3).all()
        for user, org in records:
            print(user.email, org.name_organization)
