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


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    number_group = Column(String(50), nullable=False)
    student = relationship(Student)

class Tutor(Base):
    __tablename__ = 'tutors'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    tutor_id = Column('tutor_id', ForeignKey('tutors.id', ondelete='CASCADE'))
    tutor = relationship('Tutor', backref='subjects')


class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    date_ = Column('date_', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', backref='marks')
    subject = relationship('Subject', backref='marks')


class TutorStudent(Base):
    __tablename__ = 'tutors_to_students'
    id = Column(Integer, primary_key=True)
    tutor_id = Column('tutor_id', ForeignKey('tutors.id', ondelete='CASCADE'))
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))



Base.metadata.create_all(engine)
Base.metadata.bind = engine

new_student = Student(name="Max", number_group="2")
session.add(new_student)

session.commit()

new_group = Group(number_group="23")
session.add(new_group)
session.commit()

for student in session.query(Student).all():
    print(student.name)