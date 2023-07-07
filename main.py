from sqlalchemy.orm import Session
import os
import models
from models import Users, Organizations, Objects, Projects
from database import engine

# Удаление
os.remove('prom_bez.db')
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

# Create Organization
with Session(bind=engine) as session:
    # add org

    for i in range(1, 5):
        owner_id = 1 if i < 3 else 2
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

# Create Objects
with Session(bind=engine) as session:
    # add obj
    obj1 = Objects(name_object = 'obj1',
    address_object = 'Addr1',
    reg_number_object = 'Reg1',
    class_object = 'class1')
    session.add(obj1)

    obj2 = Objects(name_object = 'obj2',
    address_object = 'Addr2',
    reg_number_object = 'Reg2',
    class_object = 'class2')
    session.add(obj2)

    session.commit()

    # add projects
    prj1 = Projects(name_project = 'Prj1',
    code_project = 'Code1',
    description_project = 'Desc1')
    session.add(prj1)

    prj2 = Projects(name_project = 'Prj2',
    code_project = 'Code2',
    description_project = 'Desc2')
    session.add(prj2)

    session.commit()

    # map obj to projects
    prj1.objects = [obj1, obj2]
    prj2.objects = [obj2]

    session.commit()

if __name__ == '__main__':
    with Session(bind=engine) as session:
        users = session.query(Users).all()
        for user in users:
            print(f"{user.id} {user.email} ({user.organizations})")

        print('_' * 30)
        orgs = session.query(Organizations).all()
        for org in orgs:
            print(f"{org.id} {org.name_organization} (user_id = {org.owner_id})")
        print('_' * 30)
        print(session.query(Objects).where(Objects.id == 1).one().projects)
        print(session.query(Projects).where(Projects.id == 1).one().objects)
