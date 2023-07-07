from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
from database import Base, engine
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True, index=True)
    company_name = Column(String)
    first_tname = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    hashed_password = Column(String)

    organizations = relationship('Organizations', back_populates='owner')


class Organizations(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    # Наименование организации
    name_organization = Column(String)
    # Должность и ФИО директора
    name_position_director = Column(String)
    name_director = Column(String)
    # Должность и ФИО технического руководителя (главный инженер)
    name_position_tech_director = Column(String)
    name_tech_director = Column(String)
    # Юридический адрес
    legal_address = Column(String)
    # Телефон
    telephone = Column(String)
    # Почта
    email = Column(String)
    # Внешний ключ на таблицу 'users' (у одного пользователя может быть несколько организаций)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('Users', back_populates='organizations')


# class Objects(Base):
#     __tablename__ = 'objects'
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование объекта (опасного производственного объекта)
#     name_object = Column(String)
#     # Адрес объекта
#     address_object = Column(String)
#     # Регистрационный номер
#     reg_number_object = Column(String)
#     # Класс опасности
#     class_object = Column(String)
#     # Внешний ключ на таблицу 'organizations' (у одной организации может быть несколько объектов)
#     owner_id = Column(Integer, ForeignKey('organizations.id'))
#     owner = relationship('Organizations', back_populates='objects')
#     # Отношение многие-ко-многим 'objects'
#     # (один проект может относится к нескольким объектам и у одного объекта может быть несколько проектов)
#     project_objects = relationship('Projects', secondary='project_objects', back_populates='objects')
#     objects_project = relationship('Projects', secondary='objects_project', back_populates='objects')
#
#
# class Projects(Base):
#     __tablename__ = 'projects'
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование проекта
#     name_project = Column(String)
#     # Шифр проекта
#     code_project = Column(String)
#     # Описание проекта
#     description_project = Column(String)
#     # Отношение многие-ко-многим 'objects'
#     # (один проект может относится к нескольким объектам и у одного объекта может быть несколько проектов)
#     project_objects = relationship('Objects', secondary='project_objects', back_populates='projects')
#     objects_project = relationship('Objects', secondary='objects_project', back_populates='projects')
#
#
# class ProjectObjects(Base):
#     __tablename__ = "project_objects"
#
#     id = Column(Integer, primary_key=True, index=True)
#     object_id = Column(Integer, ForeignKey('objects.id'))
#     project_id = Column(Integer, ForeignKey('projects.id'))
#
#
# class ObjectsProject(Base):
#     __tablename__ = "objects_project"
#
#     id = Column(Integer, primary_key=True, index=True)
#     object_id = Column(Integer, ForeignKey('objects.id'))
#     project_id = Column(Integer, ForeignKey('projects.id'))



