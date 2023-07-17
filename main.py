from sqlalchemy.orm import Session
import os
import models
from models import User, Organization, Object, Project
# Substances, Devices, Pumps, Pipelines, Compressors
from database import engine

# Удаление
try:
    os.remove('prom_bez.db')
except OSError:
    pass

# Создание таблиц по models
models.Base.metadata.create_all(bind=engine)

# Create Users
with Session(bind=engine) as session:
    # add users
    usr1 = User(email='test1@yandex.ru',
                user_name='Test1')
    session.add(usr1)

    usr2 = User(email='test2@yandex.ru',
                user_name='Test2')
    session.add(usr2)
    session.commit()

# Create Organization
with Session(bind=engine) as session:
    # add org
    for i in range(1, 5):
        org = Organization(name_organization=f'Org{i}', user_id=1 if i % 2 == 0 else 2)
        session.add(org)
    session.commit()

# Create Object Project
# Test it
with Session(bind=engine) as session:
    # add users
    obj1 = Object(org_id=1)
    session.add(obj1)

    obj2 = Object(org_id=2)
    session.add(obj2)

    session.commit()

    # add projects
    prj1 = Project()
    session.add(prj1)

    prj2 = Project()
    session.add(prj2)

    session.commit()

    # map users to projects
    prj1.objects = [obj1, obj2]
    prj2.objects = [obj1]

    session.commit()

if __name__ == '__main__':
    pass
    # with Session(bind=engine) as session:
    #     users = session.query(Users).all()
    #     for user in users:
    #         print(f"{user.id} {user.email} ({user.organizations})")
    #
    #     print('_' * 30)
    #     orgs = session.query(Organizations).all()
    #     for org in orgs:
    #         print(f"{org.id} {org.name_organization} (user_id = {org.user_id})")
    #     print('_' * 30)
    #     objs = session.query(Objects).all()
    #     for obj in objs:
    #         print(f"{obj.id} {obj.name_object} (organization_id = {obj.organization_id})")
    #     print('_' * 30)

    with Session(bind=engine) as session:
        # получаем пользователя user с id==1
        t = session.query(User).filter(User.id == 1).first()
        # удаляем
        session.delete(t)
        session.commit()
