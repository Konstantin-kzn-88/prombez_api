from sqlalchemy.orm import Session

import models
from models import Users, Organizations
from database import engine

# Удаление таблиц
Users.__table__.drop(bind=engine)
Organizations.__table__.drop(bind=engine)
# Создание таблиц по models
models.Base.metadata.create_all(bind=engine)

# Create Users
with Session(bind=engine) as session:
    # add users
    usr1 = Users(email='test1@yandex.ru',
                 user_name='Test1',
                 company_name='Company1',
                 first_tname='FirstName1',
                 last_name='LastName1',
                 phone_number='123456789',
                 hashed_password='#123654')
    session.add(usr1)

    usr2 = Users(email='test2@yandex.ru',
                 user_name='Test2',
                 company_name='Company2',
                 first_tname='FirstName2',
                 last_name='LastName2',
                 phone_number='9897654321',
                 hashed_password='#1589725')
    session.add(usr2)

    session.commit()

# Create Users
with Session(bind=engine) as session:
    # add org

    for i in range(1, 7):
        owner_id = 1 if i < 4 else 2
        org = Organizations(name_organization=f'Org{i}',
                            name_position_director=f'Dir{i}',
                            name_director=f'Name_dir{i}',
                            name_position_tech_director=f'TechDir{i}',
                            name_tech_director=f'Name_dir{i}',
                            legal_address=f'Add{i}',
                            telephone=f'Tel{i}',
                            email=f'email{i}',
                            owner_id=owner_id)
        session.add(org)
    session.commit()

    # # add projects
    # prj1 = Project(name="Project 1")
    # session.add(prj1)
    #
    # prj2 = Project(name="Project 2")
    # session.add(prj2)
    #
    # session.commit()
    #
    # # map users to projects
    # prj1.users = [usr1, usr2]
    # prj2.users = [usr2]
    #
    # session.commit()

if __name__ == '__main__':
    with Session(bind=engine) as session:
        users = session.query(Users).all()
        for user in users:
            print(f"{user.id} {user.email} ({user.organizations})")

        print('_'*30)
        orgs = session.query(Organizations).all()
        for org in orgs:
            print(f"{org.id} {org.name_organization} ({org.owner_id})")
