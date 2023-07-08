from sqlalchemy.orm import Session
import os
import models
from models import Users, Organizations, Objects
    # Objects, Projects
    # Substances, Devices, Pumps, Pipelines, Compressors
from database import engine

# Удаление
os.remove('prom_bez.db')
# Создание таблиц по models
models.Base.metadata.create_all(bind=engine)

# Create Users
with Session(bind=engine) as session:
    # add users
    usr1 = Users(email='test1@yandex.ru',
                 user_name='Test1')
    session.add(usr1)

    usr2 = Users(email='test2@yandex.ru',
                 user_name='Test2')
    session.add(usr2)
    session.commit()

# Create Organization
with Session(bind=engine) as session:
    # add org
    for i in range(1, 5):
        owner_id = 1 if i < 3 else 2
        org = Organizations(name_organization=f'Org{i}',
                            user_id=owner_id)
        session.add(org)
    session.commit()


if __name__ == '__main__':
    with Session(bind=engine) as session:
        users = session.query(Users).all()
        for user in users:
            print(f"{user.id} {user.email} ({user.organizations})")

        print('_' * 30)
        orgs = session.query(Organizations).all()
        for org in orgs:
            print(f"{org.id} {org.name_organization} (user_id = {org.user_id})")
        print('_' * 30)
        # print(session.query(Objects).where(Objects.id == 1).one().projects)
        # print(session.query(Projects).where(Projects.id == 1).one().objects)

    # with Session(bind=engine) as session:
    #     # получаем пользователя user с id==1
    #     t = session.query(Objects).filter(Objects.id == 1).first()
    #     # удаляем
    #     session.delete(t)
    #     session.commit()
