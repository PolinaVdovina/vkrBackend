# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class District(Base):
    __tablename__ = 'districts'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".districts_id_seq'::regclass)"))
    value = Column(String, nullable=False)


t_house_filter_view = Table(
    'house_filter_view', metadata,
    Column('id', BigInteger),
    Column('district', String),
    Column('street', String),
    Column('number', String),
    Column('minLayingDepth', Float),
    Column('maxLayingDepth', Float),
    schema='public'
)


t_pivot_filter_view = Table(
    'pivot_filter_view', metadata,
    Column('houseId', BigInteger),
    Column('district', String),
    Column('street', String),
    Column('number', String),
    Column('sampleId', BigInteger),
    Column('date', DateTime),
    Column('tubeId', BigInteger),
    Column('tube', String),
    Column('depth', Float),
    Column('value', Float),
    Column('quarter', BigInteger),
    Column('month', BigInteger),
    Column('day', BigInteger),
    Column('year', BigInteger),
    schema='public'
)


t_pivot_view = Table(
    'pivot_view', metadata,
    Column('house_id', BigInteger),
    Column('district', String),
    Column('street', String),
    Column('number', String),
    Column('sample_id', BigInteger),
    Column('date', DateTime),
    Column('tube_id', BigInteger),
    Column('tube', String),
    Column('id', BigInteger),
    Column('depth', Float),
    Column('value', Float),
    Column('quarter', BigInteger),
    Column('month', BigInteger),
    Column('day', BigInteger),
    Column('year', BigInteger),
    schema='public'
)


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".roles_id_seq'::regclass)"))
    value = Column(String, nullable=False)

    users = relationship('User', secondary='public.user_roles')


t_sample_filter_view = Table(
    'sample_filter_view', metadata,
    Column('id', BigInteger),
    Column('depth', Float),
    Column('value', Float),
    Column('tubeId', BigInteger),
    Column('date', DateTime),
    schema='public'
)


class Street(Base):
    __tablename__ = 'streets'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".streets_id_seq'::regclass)"))
    value = Column(String, nullable=False)


t_tube_filter_view = Table(
    'tube_filter_view', metadata,
    Column('id', BigInteger),
    Column('depth', Float),
    Column('houseId', BigInteger),
    Column('value', String),
    schema='public'
)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".users_id_seq'::regclass)"))
    login = Column(String, nullable=False)
    password_hash = Column(String)
    token_id = Column(BigInteger, server_default=text("nextval('\"public\".users_id_seq'::regclass)"))


class House(Base):
    __tablename__ = 'houses'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".houses_id_seq'::regclass)"))
    number = Column(String, nullable=False)
    street_id = Column(ForeignKey('public.streets.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    district_id = Column(ForeignKey('public.districts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    min_laying_depth = Column(Float)
    max_laying_depth = Column(Float)

    district = relationship('District')
    street = relationship('Street')


t_user_roles = Table(
    'user_roles', metadata,
    Column('user_id', ForeignKey('public.users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('role_id', ForeignKey('public.roles.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    schema='public'
)


class Tube(Base):
    __tablename__ = 'tubes'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".tubes_id_seq'::regclass)"))
    depth = Column(Float)
    house_id = Column(ForeignKey('public.houses.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    value = Column(String)

    house = relationship('House')


class TubeSample(Base):
    __tablename__ = 'tube_samples'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".tube_samples_id_seq'::regclass)"))
    depth = Column(Float)
    value = Column(Float)
    tube_id = Column(ForeignKey('public.tubes.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date = Column(DateTime, nullable=False)

    tube = relationship('Tube')
