# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from core import get_database_session

Base = declarative_base()
metadata = Base.metadata



class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".users_id_seq'::regclass)"))
    login = Column(String, nullable=False)
    password_hash = Column(String)
    token_id = Column(BigInteger, server_default=text("nextval('\"public\".users_id_seq'::regclass)"))
    roles = relationship('Role', secondary='public.user_roles')

    def create_access_token_payload(self):
        return {
            'user_id': self.id,
            'token_id': self.token_id,
        }

