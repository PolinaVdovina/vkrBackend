# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


