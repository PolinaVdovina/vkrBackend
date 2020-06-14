# coding: utf-8
from datetime import datetime

from flask_jwt_extended import create_access_token
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, SmallInteger, String, text, Date, Table, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from core import get_database_session

Base = declarative_base()
metadata = Base.metadata


def json_to_model(json, entity):
    for key, value in json.items():
        setattr(entity, key, value)
    get_database_session().commit()


class Role(Base):
    __tablename__ = 'Role'
    __table_args__ = {'schema': 'public'}

    id = Column(SmallInteger, primary_key=True)
    value = Column(String)

    @staticmethod
    def get_roles_from_string_array(roles):
        result = []
        for role in roles:
            result.append(get_database_session().query(Role).filter(Role.value == role).first())
        return result

class Enterprise(Base):
    __tablename__ = 'Enterprise'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".\"Enterprise_id_seq\"'::regclass)"))
    name = Column(String)
    address = Column(String)
    phone = Column(String)

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'value': self.value,
            'address': self.address,
            'phone': self.phone
        }


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

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'value': self.name,
            'location': self.location
        }

class Position(Base):
    __tablename__ = 'Position'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".\"Position_id_seq\"'::regclass)"))
    value = Column(String)

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'value': self.value
        }

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

    @property
    def access_token(self):
        return create_access_token({"user_id": self.id, "token_id":self.token_id, "role": self.role_id}, expires_delta=False)

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'position_id': self.position_id,
            'phone': self.phone,
            'e_mail': self.e_mail
        }

class User(Employee):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'public'}

    id = Column(ForeignKey('public.Employee.id'), primary_key=True)
    rating = Column(Float)
    building = Column(String)
    cabinet = Column(String)
    programs = Column(String)
    id_organization = Column(ForeignKey('public.Organization.id'))
    id_enterprise = Column(ForeignKey('public.Enterprise.id'))

    Enterprise = relationship('Enterprise')
    Organization = relationship('Organization')

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'position_id': self.position_id,
            'phone': self.phone,
            'e_mail': self.e_mail,
            'rating': self.rating,
            'building': self.building,
            'cabinet': self.cabinet,
            'programs': self.programs,
            'id_organization': self.id_organization,
            'id_enterprise': self.id_enterprise
        }


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

    def to_basic_dictionary(self):
        date_reg = self.date_reg
        if self.date_reg is not None:
            date_reg = self.date_reg.strftime("%d/%m/%y %H:%M")
        date_start = self.date_start
        if self.date_start is not None:
            date_start = self.date_start.strftime("%d/%m/%y %H:%M")
        date_end = self.date_end
        if self.date_end is not None:
            date_end = self.date_end.strftime("%d/%m/%y %H:%M")
        return {
            'id': self.id,
            'date_reg': date_reg,
            'date_start': date_start,
            'date_end': date_end,
            #'method': self.Method_rec.value,
            'description': self.description,
            'extra_description': self.extra_description,
            'status': self.Status.value,
            'id_user': self.id_user,
            'user': self.User.name
        }


class WorkGroup(Base):
    __tablename__ = 'Work_group'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".\"Work_group_id_seq\"'::regclass)"))
    value = Column(String)
    id_chief = Column(ForeignKey('public.Employee.id'))

    Employee = relationship('Employee')

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'value': self.value,
            'id_chief': self.id_chief
        }



class Executor(Employee):
    __tablename__ = 'Executor'
    __table_args__ = {'schema': 'public'}

    id = Column(ForeignKey('public.Employee.id'), primary_key=True)
    rating = Column(Float)
    id_work_group = Column(ForeignKey('public.Work_group.id'))
    is_testing = Column(Boolean)

    Work_group = relationship('WorkGroup')

    def to_basic_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'position_id': self.position_id,
            'phone': self.phone,
            'e_mail': self.e_mail,
            'rating': self.rating,
            'id_work_group': self.id_work_group,
            'is_testing': self.is_testing
        }


class WorkTask(Base):
    __tablename__ = 'Work_task'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, unique=True,
                server_default=text("nextval('\"public\".\"Work_task_id_seq\"'::regclass)"))
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

    def to_basic_dictionary(self):
        date_end = self.date_end
        if self.date_end is not None:
            date_end = self.date_end.strftime("%d/%m/%y %H:%M")
        date_start = self.date_start
        if self.date_start is not None:
            date_start = self.date_start.strftime("%d/%m/%y %H:%M")
        date_deadline = self.date_deadline
        if self.date_deadline is not None:
            date_deadline = self.date_deadline.strftime("%d/%m/%y %H:%M")
        if self.Executor is not None:
            executor_name = self.Executor.name
        else:
            executor_name = None
        return {
            'id': self.id,
            'description': self.description,
            'date_end': date_end,
            'id_work_group': self.id_work_group,
            'work_group': self.Work_group.value,
            'id_executor': self.id_executor,
            'executor': executor_name,
            'solution': self.solution,
            'rating_isp': self.rating_isp,
            'rating_user': self.rating_user,
            'id_incident': self.id_incident,
            'date_start': date_start,
            'date_deadline': date_deadline,
            'delay_reason': self.delay_reason,
            'priority': self.priority,
            'user': self.Incident.User.name,
            'date_reg': self.Incident.date_reg.strftime("%d/%m/%y %H:%M")
        }

