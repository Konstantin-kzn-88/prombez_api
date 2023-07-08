from sqlalchemy import ForeignKey, Column, Integer, String, Float, Table
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True, index=True)
    # Отношение к таблице Organizations
    organizations = relationship("Organizations", cascade="all, delete-orphan")


class Organizations(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    # Наименование организации
    name_organization = Column(String)
    # Внешний ключ на таблицу 'users' (у одного пользователя может быть несколько организаций)
    user_id = Column(Integer, ForeignKey('users.id'))
    # Отношение к таблице Objects
    objects = relationship("Objects", cascade="all, delete-orphan")

object_project = Table('object_project', Base.metadata,
    Column('object_id', Integer(), ForeignKey("objects.id")),
    Column('project_id', Integer(), ForeignKey("projects.id"))
)

class Objects(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    # Наименование объекта (опасного производственного объекта)
    name_object = Column(String, unique=True)
    # Внешний ключ на таблицу 'organizations' (у одной организации может быть несколько объектов)
    organization_id = Column(Integer, ForeignKey('organizations.id'))

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    # Наименование проекта
    name_project = Column(String)
    # Отношения многие ко многим object_project (у каждого объекта, может быть несколько проектов,
    # и наоборот)
    object_id = Column(Integer, ForeignKey('objects.id'))
    object = relationship("Objects", secondary=object_project, backref="projects")
    # Отношение к таблице pipelines
    pipelines = relationship("Pipelines", cascade="all, delete-orphan")
    # Отношение к таблице devices
    devices = relationship("Devices", cascade="all, delete-orphan")
    # Отношение к таблице pumps
    pumps = relationship("Pumps", cascade="all, delete-orphan")
    # Отношение к таблице compressors
    compressors = relationship("Compressors", cascade="all, delete-orphan")


class Pipelines(Base):
    __tablename__ = "pipelines"
    id = Column(Integer, primary_key=True, index=True)
    # Наименование трубопровода
    pipe_name = Column(String)
    # Внешний ключ на таблицу 'Projects' (у одного проекта может быть несколько трубопроводов)
    project_id = Column(Integer, ForeignKey('projects.id'))
    # Отношение один к многим (у одного трубопровода может быть одно вещество, но вещество может
    #быть у различного оборудования)
    sub_id = Column(Integer, ForeignKey('substances.id'))


class Devices(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    # Наименование оборудования
    dev_name = Column(String)
    # Внешний ключ на таблицу 'Projects' (у одного проекта может быть несколько оборудований)
    project_id = Column(Integer, ForeignKey('projects.id'))
    # Отношение один к многим  (у одного оборудования может быть одно вещество, но вещество может
    #быть у различного оборудования)
    sub_id = Column(Integer, ForeignKey('substances.id'))


class Pumps(Base):
    __tablename__ = "pumps"
    id = Column(Integer, primary_key=True, index=True)
    # Наименование насоса
    pump_name = Column(String)
    # Внешний ключ на таблицу 'Projects' (у одного проекта может быть несколько насосов)
    project_id = Column(Integer, ForeignKey('projects.id'))
    # Отношение один к многим (у одного насоса может быть одно вещество, но вещество может
    # быть у различного оборудования)
    sub_id = Column(Integer, ForeignKey('substances.id'))


class Compressors(Base):
    __tablename__ = "compressors"

    id = Column(Integer, primary_key=True, index=True)
    # Наименование компрессора
    compressor_name = Column(String)
    # Внешний ключ на таблицу 'Projects' (у одного проекта может быть несколько компрессоров)
    project_id = Column(Integer, ForeignKey('projects.id'))
    # Отношение один к многим (у одного компрессора может быть одно вещество, но вещество может
    # быть у различного оборудования)
    sub_id = Column(Integer, ForeignKey('substances.id'))

class Substances(Base):
    __tablename__ = "substances"

    id = Column(Integer, primary_key=True, index=True)
    # Наименование вещества
    sub_name = Column(String)

    # Отношение к таблице pipelines
    pipelines = relationship("Pipelines")
    # Отношение к таблице devices
    devices = relationship("Devices")
    # Отношение к таблице pumps
    pumps = relationship("Pumps")
    # Отношение к таблице compressors
    compressors = relationship("Compressors")




# from sqlalchemy import ForeignKey, Column, Integer, String, Float
# from database import Base
# from sqlalchemy.orm import relationship
#
#
# class Users(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     user_name = Column(String, unique=True, index=True)
#     company_name = Column(String)
#     first_tname = Column(String)
#     last_name = Column(String)
#     phone_number = Column(String)
#     hashed_password = Column(String)
#
#     organizations = relationship('Organizations', back_populates='owner', cascade="all, delete-orphan")
#
#
# class Organizations(Base):
#     __tablename__ = 'organizations'
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование организации
#     name_organization = Column(String)
#     # Должность и ФИО директора
#     name_position_director = Column(String)
#     name_director = Column(String)
#     # Должность и ФИО технического руководителя (главный инженер)
#     name_position_tech_director = Column(String)
#     name_tech_director = Column(String)
#     # Юридический адрес
#     legal_address = Column(String)
#     # Телефон
#     telephone = Column(String)
#     # Почта
#     email = Column(String)
#     # Внешний ключ на таблицу 'users' (у одного пользователя может быть несколько организаций)
#     owner_id = Column(Integer, ForeignKey('users.id'))
#     owner = relationship('Users', back_populates='organizations')
#
#     objects = relationship('Objects', back_populates='owner', cascade="all, delete-orphan")
#
#
# class Objects(Base):
#     __tablename__ = "objects"
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование объекта (опасного производственного объекта)
#     name_object = Column(String, unique=True)
#     # Адрес объекта
#     address_object = Column(String)
#     # Регистрационный номер
#     reg_number_object = Column(String, unique=True)
#     # Класс опасности
#     class_object = Column(String)
#     # связь многие ко многим
#     projects = relationship('Projects', secondary='project_object', back_populates='objects')
#     # Внешний ключ на таблицу 'Organizations' (у одной организации может быть несколько объектов)
#     owner_id = Column(Integer, ForeignKey('organizations.id'))
#     owner = relationship('Organizations', back_populates='objects')
#
#
# class Projects(Base):
#     __tablename__ = "projects"
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование проекта
#     name_project = Column(String)
#     # Шифр проекта
#     code_project = Column(String)
#     # Описание проекта
#     description_project = Column(String)
#     # связь многие ко многим
#     objects = relationship('Objects', secondary='project_object', back_populates='projects')
#     # Внешний ключ на таблицу 'Objects' (у однго объекта может быть несколько проектов)
#     owner_id = Column(Integer, ForeignKey('objects.id'))
#     owner = relationship('Objects', back_populates='projects')
#
#
# class ProjectObject(Base):
#     "Таблица связей объектов и проектов"
#     __tablename__ = "project_object"
#
#     id = Column(Integer, primary_key=True, index=True)
#     object_id = Column(Integer, ForeignKey('objects.id'))
#     project_id = Column(Integer, ForeignKey('projects.id'))
#
#
# class Substances(Base):
#     __tablename__ = "substances"
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование вещества
#     sub_name = Column(String)
#     # Тип вещества (0 - ГЖ, 1 - СУГ; 2 - ГЖ с токси, 3- СУГ с токси, 4 - токси)
#     sub_type = Column(Integer)
#     # Плотность вещества, кг/м3
#     sub_density_liguid = Column(Integer)
#     # Плотность газовой фазы, кг/м3
#     sub_density_gas = Column(Float)
#     # Мол.масса, кг/кмоль
#     sub_mol_weight = Column(Float)
#     # Давление пара, кПа
#     sub_steam_pressure = Column(Integer)
#     # Температура вспышки, град С
#     sub_flash_temp = Column(Integer)
#     # Температура кипения, град С
#     sub_boiling_temp = Column(Integer)
#     # Теплота испарения, Дж/кг
#     sub_evaporation_heat = Column(Integer)
#     # Теплоемкость жидкости, Дж/(кг*К)
#     sub_heat_capacity = Column(Integer)
#     # Класс вещества (для взрыва (1,2,3,4))
#     sub_class = Column(Integer)
#     # Теплота сгорания, кДж/кг
#     sub_heat_combustion_temp = Column(Integer)
#     # Параметр сигма (для взрыва (4 - гетерогенная смесь, 7 - гомогенная смесь)
#     sub_sigma = Column(Integer)
#     # Энергозапас (для взрыва (2 - облако тяжелого газа лежит на земле, 1 - не лежит на земле)
#     sub_energy_level = Column(Integer)
#     # Нижний концентрационный предел взрываемости, об.%
#     sub_lower_conc = Column(Integer)
#
#
# class Pipelines(Base):
#     __tablename__ = "pipelines"
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование трубопровода
#     pipe_name = Column(String)
#     # Длина трубопровода, км
#     pipe_lenght = Column(Float)
#     # Диаметр трубопровода, мм
#     pipe_diameter = Column(Float)
#     # Давление трубопровода, МПа
#     pipe_pressure = Column(Float)
#     # Температура трубопровода, град С
#     pipe_temp = Column(Float)
#     # Расход трубопровода, м3/ч
#     pipe_flow = Column(Float)
#     # Время остановки прокачки, с
#     pipe_shutdown = Column(Integer)
#     # Тип окружающего пространства (для взрыва от 1 до 4)
#     pipe_view_space = Column(Integer)
#     # Прогнозируемое количество погибших, чел
#     pipe_death_man = Column(Integer)
#     # Прогнозируемое количество пострадавших, чел
#     pipe_injured_man = Column(Integer)
#
#
# class Devices(Base):
#     __tablename__ = "devices"
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование оборудования
#     dev_name = Column(String)
#     # Объем оборудования, м3
#     dev_volume = Column(Float)
#     # Доля заполнения оборудования, (доли единицы)
#     dev_complection = Column(Float)
#     # Расход  подводящего трубопровода, м3/ч
#     dev_flow = Column(Float)
#     # Время остановки прокачки, с
#     dev_shutdown = Column(Integer)
#     # Давление оборудования, МПа
#     dev_pressure = Column(Float)
#     # Температура оборудования, град С
#     dev_temp = Column(Float)
#     # Поддон оборудования, м2
#     dev_spill = Column(Integer)
#     # Тип окружающего пространства (для взрыва от 1 до 4)
#     dev_view_space = Column(Integer)
#     # Прогнозируемое количество погибших, чел
#     dev_death_man = Column(Integer)
#     # Прогнозируемое количество пострадавших, чел
#     dev_injured_man = Column(Integer)
#
#
# class Pumps(Base):
#     __tablename__ = "pumps"
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование насоса
#     pump_name = Column(String)
#     # Расход  подводящего трубопровода, м3/ч
#     pump_flow = Column(Float)
#     # Время остановки прокачки, с
#     pump_shutdown = Column(Integer)
#     # Температура насоса, град С
#     pump_temp = Column(Float)
#     # Тип окружающего пространства (для взрыва от 1 до 4)
#     pump_view_space = Column(Integer)
#     # Прогнозируемое количество погибших, чел
#     pump_death_man = Column(Integer)
#     # Прогнозируемое количество пострадавших, чел
#     pump_injured_man = Column(Integer)
#
#
# class Compressors(Base):
#     __tablename__ = "compressors"
#
#     id = Column(Integer, primary_key=True, index=True)
#     # Наименование компрессора
#     compressor_name = Column(String)
#     # Расход  компрессора трубопровода, м3/ч
#     compressor_flow = Column(Float)
#     # Время остановки прокачки, с
#     compressor_shutdown = Column(Integer)
#     # Температура компрессора, град С
#     compressor_temp = Column(Float)
#     # Тип окружающего пространства (для взрыва от 1 до 4)
#     compressor_view_space = Column(Integer)
#     # Прогнозируемое количество погибших, чел
#     compressor_death_man = Column(Integer)
#     # Прогнозируемое количество пострадавших, чел
#     compressor_injured_man = Column(Integer)
