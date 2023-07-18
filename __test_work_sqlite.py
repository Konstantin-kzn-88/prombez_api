from sqlalchemy.orm import Session
import os
import models
from models import User, Organization, Object, Project, Pipeline, Device, Pump, Substance
from database import engine

# Удаление
try:
    os.remove('prom_bez.db')
except OSError:
    pass

# Создание таблиц по models
models.Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    # Create Users
    with Session(bind=engine) as session:
        # add users
        usr1 = User(email='test1@yandex.ru',
                    user_name='Test1',
                    company_name='TestComp1',
                    first_name='FName1',
                    last_name='LName2',
                    phone_number='+9178889569',
                    hashed_password='#1s34!0-t'
                    )
        session.add(usr1)

        usr2 = User(email='test2@yandex.ru',
                    user_name='Test2',
                    company_name='TestComp2',
                    first_name='FName2',
                    last_name='LName2',
                    phone_number='+9272586979',
                    hashed_password='fr5!{]11!'
                    )
        session.add(usr2)
        session.commit()

    # Create Organization
    with Session(bind=engine) as session:
        # add org
        org1 = Organization(name_organization='Org1',
                            name_position_director='Director1',
                            name_director='Ivanov Ivan',
                            name_position_tech_director='TechDir1',
                            name_tech_director='Peterov Petr',
                            legal_address='Moscow City',
                            telephone='+8965558791',
                            email='org1@mail.ru',
                            user_id=1
                            )
        session.add(org1)

        org2 = Organization(name_organization='Org2',
                            name_position_director='GenDirector2',
                            name_director='Smirnov Ivan',
                            name_position_tech_director='TechDir2',
                            name_tech_director='Kuznetsov Petr',
                            legal_address='Kazan City',
                            telephone='+8435556969',
                            email='org2@mail.ru',
                            user_id=2
                            )
        session.add(org2)
        session.commit()

# Create Object Project
# Test it
with Session(bind=engine) as session:
    # add users
    obj1 = Object(name_object='Kyzaikinskoe mestorohzdenie',
                  address_object='Almet region',
                  reg_number_object='A43-5896-001',
                  class_object='II',
                  org_id=1)
    session.add(obj1)

    obj2 = Object(name_object='Akanskoe mestorohzdenie',
                  address_object='Cheremshan region',
                  reg_number_object='A43-4789-001',
                  class_object='II', org_id=2)
    session.add(obj2)

    session.commit()

    # add projects
    prj1 = Project(name_project='Project1',
                   code_project='98-2021',
                   description_project='About project')
    session.add(prj1)

    prj2 = Project(name_project='Project2',
                   code_project='25-25',
                   description_project='About project')
    session.add(prj2)

    prj3 = Project(name_project='Project3',
                   code_project='33-2021',
                   description_project='About project')
    session.add(prj3)

    prj4 = Project(name_project='Project4',
                   code_project='25-58',
                   description_project='About project')
    session.add(prj4)

    session.commit()

    # map users to projects
    obj1.projects = [prj1, prj3]
    obj2.projects = [prj2, prj4]

    session.commit()

# Create Sub
with Session(bind=engine) as session:
    sub1 = Substance(sub_name='neft1',
                     sub_density_liguid=850,
                     sub_density_gas=3,
                     sub_mol_weight=210,
                     sub_steam_pressure=35,
                     sub_flash_temp=13,
                     sub_boiling_temp=350,
                     sub_evaporation_heat=369000,
                     sub_heat_capacity=2100,
                     sub_class=3,
                     sub_heat_combustion_temp=46000,
                     sub_sigma=7,
                     sub_energy_level=2,
                     sub_lower_conc=3.56)
    session.add(sub1)

    sub2 = Substance(sub_name='neft2',
                     sub_density_liguid=950,
                     sub_density_gas=3,
                     sub_mol_weight=200,
                     sub_steam_pressure=35,
                     sub_flash_temp=13,
                     sub_boiling_temp=350,
                     sub_evaporation_heat=400000,
                     sub_heat_capacity=2100,
                     sub_class=3,
                     sub_heat_combustion_temp=47000,
                     sub_sigma=7,
                     sub_energy_level=2,
                     sub_lower_conc=3.21)
    session.add(sub2)

    sub3 = Substance(sub_name='neft3',
                    sub_density_liguid=967,
                    sub_density_gas=3,
                    sub_mol_weight=190,
                    sub_steam_pressure=35,
                    sub_flash_temp=13,
                    sub_boiling_temp=333,
                    sub_evaporation_heat=370658,
                    sub_heat_capacity=2100,
                    sub_class=3,
                    sub_heat_combustion_temp=48000,
                    sub_sigma=7,
                    sub_energy_level=2,
                    sub_lower_conc=3.22)
    session.add(sub3)

    session.commit()
