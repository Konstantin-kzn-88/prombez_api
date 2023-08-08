from sqlalchemy.orm import Session
import os
import models
from models import User, Organization, Object, Project, Pipeline, Device, Pump, Substance
from database import engine
import itertools
from random import randint, randrange

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

# # Create Object Project
# # Test it
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
                   description_project='About project',
                   object_id=1)
    session.add(prj1)

    prj2 = Project(name_project='Project2',
                   code_project='25-25',
                   description_project='About project',
                   object_id=1)
    session.add(prj2)

    prj3 = Project(name_project='Project3',
                   code_project='33-2021',
                   description_project='About project',
                   object_id=2)
    session.add(prj3)

    prj4 = Project(name_project='Project4',
                   code_project='25-58',
                   description_project='About project',
                   object_id=2)
    session.add(prj4)

    session.commit()


#
# # Create Sub
# with Session(bind=engine) as session:
#     sub1 = Substance(sub_name='neft1',
#                      sub_density_liguid=850,
#                      sub_density_gas=3,
#                      sub_mol_weight=210,
#                      sub_steam_pressure=35,
#                      sub_flash_temp=13,
#                      sub_boiling_temp=350,
#                      sub_evaporation_heat=369000,
#                      sub_heat_capacity=2100,
#                      sub_class=3,
#                      sub_heat_combustion_temp=46000,
#                      sub_sigma=7,
#                      sub_energy_level=2,
#                      sub_lower_conc=3.56)
#     session.add(sub1)
#
#     sub2 = Substance(sub_name='neft2',
#                      sub_density_liguid=950,
#                      sub_density_gas=3,
#                      sub_mol_weight=200,
#                      sub_steam_pressure=35,
#                      sub_flash_temp=13,
#                      sub_boiling_temp=350,
#                      sub_evaporation_heat=400000,
#                      sub_heat_capacity=2100,
#                      sub_class=3,
#                      sub_heat_combustion_temp=47000,
#                      sub_sigma=7,
#                      sub_energy_level=2,
#                      sub_lower_conc=3.21)
#     session.add(sub2)
#
#     sub3 = Substance(sub_name='neft3',
#                      sub_density_liguid=967,
#                      sub_density_gas=3,
#                      sub_mol_weight=190,
#                      sub_steam_pressure=35,
#                      sub_flash_temp=13,
#                      sub_boiling_temp=333,
#                      sub_evaporation_heat=370658,
#                      sub_heat_capacity=2100,
#                      sub_class=3,
#                      sub_heat_combustion_temp=48000,
#                      sub_sigma=7,
#                      sub_energy_level=2,
#                      sub_lower_conc=3.22)
#     session.add(sub3)
#
#     session.commit()
#
# # Create Pipeline
# with Session(bind=engine) as session:
#     # add pipe
#     tuple_project_id = itertools.cycle((1, 2, 3, 4))
#
#     for i in range(0, 17):
#         pipe = Pipeline(pipe_name=f'pipe{i}',
#                         pipe_lenght=randint(1, 5),
#                         pipe_diameter=114,
#                         pipe_pressure=0.35,
#                         pipe_temp=10,
#                         pipe_flow=randint(12, 30),
#                         pipe_shutdown=120,
#                         pipe_view_space=4,
#                         pipe_death_man=1,
#                         pipe_injured_man=randint(1, 2),
#                         project_id=next(tuple_project_id),
#                         substance_id=randint(1, 3)
#                         )
#         session.add(pipe)
#     session.commit()
#
# # Create Device
# with Session(bind=engine) as session:
#     # add dev
#     tuple_project_id = itertools.cycle((1, 2, 3, 4))
#
#     for i in range(0, 17):
#         dev = Device(dev_name=f'dev{i}',
#                      dev_volume=randrange(100, 2000, 100),
#                      dev_complection=0.8,
#                      dev_flow=12,
#                      dev_shutdown=120,
#                      dev_pressure=0.3,
#                      dev_temp=randrange(10, 50, 5),
#                      dev_spill=randrange(100, 2000, 100) * 20,
#                      dev_view_space=3,
#                      dev_death_man=2,
#                      dev_injured_man=randint(1, 3),
#                      project_id=next(tuple_project_id),
#                      substance_id=randint(1, 3)
#                      )
#         session.add(dev)
#     session.commit()
#
# # Create Pump
# with Session(bind=engine) as session:
#     # add pump
#     tuple_project_id = itertools.cycle((1, 2, 3, 4))
#
#     for i in range(0, 17):
#         pump = Pump(pump_name=f'pump{i}',
#                     pump_flow=randint(12, 20),
#                     pump_shutdown=120,
#                     pump_temp=30,
#                     pump_view_space=3,
#                     pump_death_man=1,
#                     pump_injured_man=1,
#                     project_id=next(tuple_project_id),
#                     substance_id=randint(1, 3)
#                     )
#         session.add(pump)
#     session.commit()
#
#
with Session(bind=engine) as session:
    usr = session.query(User).filter(User.id == 1).one()
    session.delete(usr)
    session.commit()

# _____________________________________________
# Удаление многие ко многим
# _____________________________________________
# with Session(bind=engine) as session:
#
#     obj = session.query(Object).filter(Object.id == 2).one()
#     for ass in obj.projects:
#         session.delete(ass)
#     session.delete(obj)
#     session.commit()
# ________________________________________________
