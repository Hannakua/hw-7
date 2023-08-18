from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.sqltypes import Date


# url = f'postgresql://postgres:sagan@localhost:5432/sqlalchemy_study.db'       #url = f'postgresql://{username}:{password}@{domain}:5432/{db_name}'
url = 'sqlite:///sqlalchemy_study.db'
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    number_group = Column(String(50), ForeignKey('groups.id'))
    group = relationship('Group', back_populates='student')
    # marks = relationship('Mark', back_populates='student')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    number_group = Column(String(50), nullable=False)
    student = relationship('Student', back_populates='group')

class Tutor(Base):
    __tablename__ = 'tutors'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # subjects = relationship('Subject', backref='tutor')

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    tutor_id = Column('tutor_id', ForeignKey('tutors.id', ondelete='CASCADE'))
    tutor = relationship('Tutor', backref='subjects')
    # marks = relationship('Mark', back_populates='subject')

class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    date_ = Column('date_', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', backref='marks')
    subject = relationship('Subject', backref='marks')

