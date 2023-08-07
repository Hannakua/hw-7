from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgres:///sqlalchemy_study.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    number_group = Column(String(50), ForeignKey('groups.id'))


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    number_group = Column(String(50), nullable=False)
    student = relationship(Student)

Base.metadata.create_all(engine)
Base.metadata.bind = engine

new_student = Student(name="Anton", number_group="1")
session.add(new_student)

session.commit()

new_group = Group(number_group="23")
session.add(new_group)
session.commit()

for student in session.query(Student).all():
    print(student.name)