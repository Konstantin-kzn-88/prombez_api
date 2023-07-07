from sqlalchemy import ForeignKey, Column, Integer, String
from database import Base
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

    organizations = relationship('Organizations', back_populates='owner', cascade="all, delete-orphan")


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

    objects = relationship('Objects', back_populates='owner', cascade="all, delete-orphan")
    projects = relationship('Projects', back_populates='owner', cascade="all, delete-orphan")



class Objects(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    # Наименование объекта (опасного производственного объекта)
    name_object = Column(String)
    # Адрес объекта
    address_object = Column(String)
    # Регистрационный номер
    reg_number_object = Column(String)
    # Класс опасности
    class_object = Column(String)
    # связь многие ко многим
    projects = relationship('Projects', secondary='project_object', back_populates='objects')
    # Внешний ключ на таблицу 'Organizations' (у одной организации может быть несколько объектов)
    owner_id = Column(Integer, ForeignKey('organizations.id'))
    owner = relationship('Organizations', back_populates='objects')


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    # Наименование проекта
    name_project = Column(String)
    # Шифр проекта
    code_project = Column(String)
    # Описание проекта
    description_project = Column(String)
    # связь многие ко многим
    objects = relationship('Objects', secondary='project_object', back_populates='projects')
    # Внешний ключ на таблицу 'Organizations' (у одной организации может быть несколько проектов)
    owner_id = Column(Integer, ForeignKey('organizations.id'))
    owner = relationship('Organizations', back_populates='projects')


class ProjectObject(Base):
    "Таблица связей объектов и проектов"
    __tablename__ = "project_object"

    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))


