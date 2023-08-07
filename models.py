from sqlalchemy import ForeignKey, Column, Integer, String, Float, Table
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True, index=True)
    company_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    hashed_password = Column(String)
    # Отношение один-ко-многим к таблице Organization
    organizations = relationship("Organization", back_populates="users", cascade="all, delete-orphan")


class Organization(Base):
    __tablename__ = "org_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    # Отношение к таблице User
    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    users = relationship("User", back_populates="organizations")
    # Отношение один-ко-многим к таблице Object
    objects = relationship("Object", back_populates="organizations", cascade="all, delete-orphan")
    # Отношение один-ко-многим к таблице Project
    projects = relationship("Project", back_populates="organizations", cascade="all, delete-orphan")


class Object(Base):
    __tablename__ = "object_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Наименование объекта (опасного производственного объекта)
    name_object = Column(String)
    # Адрес объекта
    address_object = Column(String)
    # Регистрационный номер
    reg_number_object = Column(String)
    # Класс опасности
    class_object = Column(String)
    # Отношение к таблице Project один-к-одному
    projects = relationship("Project", back_populates="objects", uselist=False)
    # Отношение к таблице Organization
    org_id = Column(Integer, ForeignKey("org_table.id"))
    organizations = relationship("Organization", back_populates="objects")

class Project(Base):
    __tablename__ = "project_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Наименование проекта
    name_project = Column(String)
    # Шифр проекта
    code_project = Column(String)
    # Описание проекта
    description_project = Column(String)
    # Отношение к таблице Organization
    org_id = Column(Integer, ForeignKey("org_table.id"))
    organizations = relationship("Organization", back_populates="projects")
    # Отношение один-к-одному
    object_id = Column(Integer, ForeignKey("object_table.id"))
    objects = relationship("Object", back_populates="projects")
    # Отношение один-ко-многим к таблице Pipeline
    pipelines = relationship("Pipeline", back_populates="projects", cascade="all, delete-orphan")
    # Отношение один-ко-многим к таблице Device
    devices = relationship("Device", back_populates="projects", cascade="all, delete-orphan")
    # Отношение один-ко-многим к таблице Pump
    pumps = relationship("Pump", back_populates="projects", cascade="all, delete-orphan")



class Pipeline(Base):
    __tablename__ = "pipeline_table"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Наименование трубопровода
    pipe_name = Column(String)
    # Длина трубопровода, км
    pipe_lenght = Column(Float)
    # Диаметр трубопровода, мм
    pipe_diameter = Column(Float)
    # Давление трубопровода, МПа
    pipe_pressure = Column(Float)
    # Температура трубопровода, град С
    pipe_temp = Column(Integer)
    # Расход трубопровода, м3/ч
    pipe_flow = Column(Float)
    # Время остановки прокачки, с
    pipe_shutdown = Column(Integer)
    # Тип окружающего пространства (для взрыва от 1 до 4)
    pipe_view_space = Column(Integer)
    # Прогнозируемое количество погибших, чел
    pipe_death_man = Column(Integer)
    # Прогнозируемое количество пострадавших, чел
    pipe_injured_man = Column(Integer)
    # Отношение к таблице Project
    project_id = Column(Integer, ForeignKey("project_table.id"))
    projects = relationship("Project", back_populates="pipelines")
    # Отношение один-к-одному
    substance_id = Column(Integer, ForeignKey("substance_table.id"))
    substances = relationship("Substance", back_populates="pipelines")


class Device(Base):
    __tablename__ = "device_table"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Наименование оборудования
    dev_name = Column(String)
    # Объем оборудования, м3
    dev_volume = Column(Float)
    # Доля заполнения оборудования, (доли единицы)
    dev_complection = Column(Float)
    # Расход  подводящего трубопровода, м3/ч
    dev_flow = Column(Float)
    # Время остановки прокачки, с
    dev_shutdown = Column(Integer)
    # Давление оборудования, МПа
    dev_pressure = Column(Float)
    # Температура оборудования, град С
    dev_temp = Column(Float)
    # Поддон оборудования, м2
    dev_spill = Column(Integer)
    # Тип окружающего пространства (для взрыва от 1 до 4)
    dev_view_space = Column(Integer)
    # Прогнозируемое количество погибших, чел
    dev_death_man = Column(Integer)
    # Прогнозируемое количество пострадавших, чел
    dev_injured_man = Column(Integer)
    # Отношение к таблице Project
    project_id = Column(Integer, ForeignKey("project_table.id"))
    projects = relationship("Project", back_populates="devices")
    # Отношение один-к-одному
    substance_id = Column(Integer, ForeignKey("substance_table.id"))
    substances = relationship("Substance", back_populates="devices")


class Pump(Base):
    __tablename__ = "pump_table"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Наименование насоса
    pump_name = Column(String)
    # Расход  подводящего трубопровода, м3/ч
    pump_flow = Column(Float)
    # Время остановки прокачки, с
    pump_shutdown = Column(Integer)
    # Температура насоса, град С
    pump_temp = Column(Float)
    # Тип окружающего пространства (для взрыва от 1 до 4)
    pump_view_space = Column(Integer)
    # Прогнозируемое количество погибших, чел
    pump_death_man = Column(Integer)
    # Прогнозируемое количество пострадавших, чел
    pump_injured_man = Column(Integer)
    # Отношение к таблице Project
    project_id = Column(Integer, ForeignKey("project_table.id"))
    projects = relationship("Project", back_populates="pumps")
    # Отношение один-к-одному
    substance_id = Column(Integer, ForeignKey("substance_table.id"))
    substances = relationship("Substance", back_populates="pumps")


class Substance(Base):
    __tablename__ = "substance_table"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Наименование вещества
    sub_name = Column(String)
    # Плотность вещества, кг/м3
    sub_density_liguid = Column(Integer)
    # Плотность газовой фазы при н.у., кг/м3
    sub_density_gas = Column(Float)
    # Мол.масса, кг/кмоль
    sub_mol_weight = Column(Float)
    # Давление пара, кПа
    sub_steam_pressure = Column(Integer)
    # Температура вспышки, град С
    sub_flash_temp = Column(Integer)
    # Температура кипения, град С
    sub_boiling_temp = Column(Integer)
    # Теплота испарения, Дж/кг
    sub_evaporation_heat = Column(Integer)
    # Теплоемкость жидкости, Дж/(кг*К)
    sub_heat_capacity = Column(Integer)
    # Класс вещества (для взрыва (1,2,3,4))
    sub_class = Column(Integer)
    # Теплота сгорания, кДж/кг
    sub_heat_combustion_temp = Column(Integer)
    # Параметр сигма (для взрыва (4 - гетерогенная смесь, 7 - гомогенная смесь)
    sub_sigma = Column(Integer)
    # Энергозапас (для взрыва (2 - облако тяжелого газа лежит на земле, 1 - не лежит на земле)
    sub_energy_level = Column(Integer)
    # Нижний концентрационный предел взрываемости, об.%
    sub_lower_conc = Column(Float)
    # отношение к таблице Pipeline
    pipelines = relationship("Pipeline", back_populates="substances", uselist=False)
    # отношение к таблице Device
    devices = relationship("Device", back_populates="substances", uselist=False)
    # отношение к таблице Pump
    pumps = relationship("Pump", back_populates="substances", uselist=False)

#
#
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
