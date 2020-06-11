# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, Float, ForeignKey, Integer, SmallInteger, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Enterprise(Base):
    __tablename__ = 'Enterprise'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".\"Enterprise_id_seq\"'::regclass)"))
    name = Column(String)
    address = Column(String)
    phone = Column(String)


class MethodRec(Base):
    __tablename__ = 'Method_rec'
    __table_args__ = {'schema': 'public'}

    id = Column(SmallInteger, primary_key=True)
    value = Column(String)


class Organization(Base):
    __tablename__ = 'Organization'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".\"Organization_id_seq\"'::regclass)"))
    name = Column(String)
    location = Column(String)


class Position(Base):
    __tablename__ = 'Position'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".\"Position_id_seq\"'::regclass)"))
    value = Column(String)


class Role(Base):
    __tablename__ = 'Role'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    value = Column(String)


class Status(Base):
    __tablename__ = 'Status'
    __table_args__ = {'schema': 'public'}

    id = Column(SmallInteger, primary_key=True)
    value = Column(String)


class Employee(Base):
    __tablename__ = 'Employee'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, unique=True, server_default=text("nextval('\"public\".\"Employee_id_seq\"'::regclass)"))
    name = Column(String)
    login = Column(String)
    password_hash = Column(String)
    token_id = Column(BigInteger, server_default=text("nextval('\"public\".token_id_seq'::regclass)"))
    role_id = Column(ForeignKey('public.Role.id'))
    position_id = Column(ForeignKey('public.Position.id'))
    phone = Column(String)
    e_mail = Column('e-mail', String)

    position = relationship('Position')
    role = relationship('Role')


class User(Employee):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'public'}

    id = Column(ForeignKey('public.Employee.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    rating = Column(Float)
    building = Column(String)
    cabinet = Column(String)
    programs = Column(String)
    id_organization = Column(ForeignKey('public.Organization.id'))
    id_enterprise = Column(ForeignKey('public.Enterprise.id'))

    Enterprise = relationship('Enterprise')
    Organization = relationship('Organization')


class Executor(Employee):
    __tablename__ = 'Executor'
    __table_args__ = {'schema': 'public'}

    id = Column(ForeignKey('public.Employee.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    rating = Column(Float)
    id_work_group = Column(ForeignKey('public.Work_group.id'))
    is_testing = Column(Boolean)

    Work_group = relationship('WorkGroup')


class WorkGroup(Base):
    __tablename__ = 'Work_group'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".\"Work_group_id_seq\"'::regclass)"))
    value = Column(String)
    id_chief = Column(ForeignKey('public.Employee.id'))

    Employee = relationship('Employee')


class Equipment(Base):
    __tablename__ = 'Equipment'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".\"Equipment_id_seq\"'::regclass)"))
    id_user = Column(ForeignKey('public.User.id'))
    inv_number = Column(Integer)
    start_exp_date = Column(Date)
    price = Column(Integer)
    description = Column(String)

    User = relationship('User')


class Incident(Base):
    __tablename__ = 'Incident'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".\"Incident_id_seq\"'::regclass)"))
    date_reg = Column(Date)
    date_start = Column(Date)
    date_end = Column(Date)
    id_method = Column(ForeignKey('public.Method_rec.id'))
    description = Column(String)
    extra_description = Column(String)
    id_status = Column(ForeignKey('public.Status.id'))
    id_user = Column(ForeignKey('public.User.id'))

    Method_rec = relationship('MethodRec')
    Status = relationship('Status')
    User = relationship('User')


class WorkTask(Base):
    __tablename__ = 'Work_task'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".\"Work_task_id_seq\"'::regclass)"))
    id_incident = Column(ForeignKey('public.Incident.id'))
    id_work_group = Column(ForeignKey('public.Work_group.id'))
    date_start = Column(Date)
    date_end = Column(Date)
    date_deadline = Column(Date)
    description = Column(String)
    solution = Column(String)
    delay_reason = Column(String)
    priority = Column(Float)
    id_executor = Column(ForeignKey('public.Executor.id'))
    rating_isp = Column(Float)
    rating_user = Column(Float)

    Executor = relationship('Executor')
    Incident = relationship('Incident')
    Work_group = relationship('WorkGroup')
