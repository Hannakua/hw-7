from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from models import Tutor, Student, Subject, Mark, Group, session


"""
Створюємо свою ф-цію для отримання списку дат, у які відбувається навчальний процес.
Для спрощення викидаємо тільки дні, які потрапляють на вихідні.
"""

def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    print(result)
    return result


def fill_data():
    subjects_list = ['math', 'art', 'physics', 'philosophy', 'history', 'chemistry', 'economics', 'astronomy']

    groups = ['A1', 'SA3', 'GT5']
    fake = faker.Faker()
    number_of_tutors = 5
    number_of_students = 45

    def seed_tutors():
        for _ in range(number_of_tutors):
            tutor = Tutor(name=fake.name())
            print(tutor)
            session.add(tutor)
        session.commit()

    def seed_subjects():
        tutors = session.scalars(select(Tutor.id)).all()
        for subject in subjects_list:
            session.add(Subject(name=subject, tutor_id=choice(tutors)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(number_group=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(name=fake.name(), number_group=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_marks():
        start_date = datetime.strptime("2023-02-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-07-15", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        subjects_id = session.scalars(select(Subject.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for student_id in student_ids:
            for _ in range(20):
                mark = Mark(
                    mark=randint(1, 12),
                    date_=choice(d_range),
                    student_id=student_id,
                    subject_id=choice(subjects_id),
                )
                session.add(mark)
        session.commit()

    seed_tutors()
    seed_subjects()
    seed_groups()
    seed_students()
    seed_marks()


if __name__ == "__main__":
    print('qwert')
    fill_data()

