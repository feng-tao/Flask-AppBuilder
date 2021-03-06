import datetime
from flask import g
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Table
from sqlalchemy.orm import relationship, relation
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder import Model

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class Company(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_user_company = Table('ab_user_company', Model.metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('company_id', Integer, ForeignKey('company.id')),
                                  Column('myuser_id', Integer, ForeignKey('ab_user.id'))
)


class MyUser(User):
    emp_number = Column(String(150))
    companies = relationship('Company', secondary=assoc_user_company, backref='MyUser')


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            # log.warning("AuditMixin Get User ID {0}".format(str(e)))
            return None

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender")
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)

    @declared_attr
    def created_by_fk(cls):
        return Column(Integer, ForeignKey('ab_user.id'),
                      default=cls.get_user_id, nullable=False)

    @declared_attr
    def created_by(cls):
        return relationship("MyUser", primaryjoin='%s.created_by_fk == MyUser.id' % cls.__name__, enable_typechecks=False)

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)
       
    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            # log.warning("AuditMixin Get User ID {0}".format(str(e)))
            return None 
