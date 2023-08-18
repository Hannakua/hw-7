from sqlalchemy import func, desc, select, and_

from models import Tutor, Student, Subject, Mark, Group, session


def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    :return: list[dict]
    """
    result = session.query(Student.name, func.round(func.avg(Mark.mark), 2).label('avg_mark')) \
        .select_from(Mark).join(Student).group_by(Student.id).order_by(desc('avg_mark')).limit(5).all()
    return result

def select_2(subject_):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    :return: list[dict]

    SELECT st.name as student_name, AVG(m.mark) AS average_mark, subj.name  
    FROM students as st, subjects AS subj
    INNER JOIN marks AS m ON st.id = m.student_id  AND m.subject_id  = subj.id
    WHERE subj.name = 'astronomy' 
    GROUP BY st.id
    ORDER BY average_mark DESC
    LIMIT 1;
    """
    result = session.query(Subject.name, Student.name, func.round(func.avg(Mark.mark), 2).label('avg_mark')) \
        .select_from(Mark).join(Student).join(Subject).filter(Subject.name == subject_).group_by(Student.id).order_by(desc('avg_mark')).limit(1).all()

    return result

def select_3(subject_):
    """
    Знайти середній бал у групах з певного предмета.
    :return: list[dict]

    SELECT g.number_group, AVG(m.mark) AS average_mark, s.name 
    FROM students AS st, subjects AS s
    INNER JOIN marks AS m ON st.id = m.student_id  AND m.subject_id  = s.id
    INNER JOIN groups AS g ON g.id = st.number_group 
    WHERE s.name = 'physics'  
    GROUP BY g.number_group;
    """
    result = session.query(Subject.name, Group.number_group, func.round(func.avg(Mark.mark), 2).label('avg_mark')) \
        .select_from(Mark).join(Student).join(Group).join(Subject).filter(Subject.name == subject_).group_by(Group.number_group).all()

    return result

def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    :return: list[dict]

    SELECT AVG(mark) AS average_mark
    FROM marks;
    """
    result = session.query(func.round(func.avg(Mark.mark), 2).label('avg_mark')) \
        .select_from(Mark).all()
    return result

def select_5(tutor_):
    """
    Знайти які курси читає певний викладач.
    :return: list[dict]

    SELECT t.name, s.name  
    FROM subjects AS s 
    INNER JOIN tutors AS t ON t.id  = s.tutor_id 
    WHERE t.name  = "Kelly Ramirez";
    """
    result = session.query(Tutor.name, Subject.name) \
        .select_from(Subject).join(Tutor).filter(Tutor.name == tutor_).order_by(Subject.name).all()
    return result

def select_6(group_):
    """
    Знайти список студентів у певній групі.
    :return: list[dict]

    SELECT s.name  
    from students s
    INNER JOIN groups AS g ON g.id  = s.number_group  
    WHERE g.number_group = 'GT5';
    """
    result = session.query(Student.name) \
        .select_from(Student).join(Group).filter(Group.number_group == group_).order_by(Student.name).all()

    return result

def select_7(group_, subject_):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    :return: list[dict]

    SELECT s2.name , g.number_group, m.mark, m.date_  
    from students s2, subjects AS s
    INNER JOIN groups AS g ON g.id  = s2.number_group 
    INNER JOIN marks AS m ON m.student_id  = s2.id 
    WHERE g.number_group = 'GT5' AND s.name  = "physics" 
    ORDER BY m.date_;
    """
    result = session.query(Student.name, Group.number_group, Mark.mark, Mark.date_) \
        .select_from(Student).join(Mark).join(Subject).filter(Subject.name==subject_).join(Group).filter(Group.number_group == group_).order_by(Student.name).all()

    return result


def select_8(tutor_):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    :return: list[dict]

    SELECT t.name , s.name, AVG(m.mark)
    FROM subjects AS s 
    INNER JOIN marks AS m ON m.subject_id = s.id 
    INNER JOIN tutors AS t ON t.id = s.tutor_id  
    WHERE t.name  = "Dylan Holloway" 
    GROUP BY s.name ;
    """
    result = session.query(Tutor.name, Subject.name, func.round(func.avg(Mark.mark), 2).label('avg_mark')) \
        .select_from(Mark).join(Subject).join(Tutor).filter(Tutor.name==tutor_).group_by(Subject.name).all()

    return result

def select_9(student_):
    """
    Знайти список курсів, які відвідує певний студент.
    :return: list[dict]

    SELECT s2.name, s.name 
    FROM marks AS m
    INNER JOIN subjects AS s ON m.subject_id= s.id   
    INNER JOIN students AS s2 ON s2.id = m.student_id
    WHERE  s2.name = 'Sabrina Wallace' 
    GROUP BY s.name;
    """
    result = session.query(Subject.name) \
        .select_from(Mark).join(Subject).join(Student).filter(Student.name==student_).group_by(Subject.name).all()

    return {student_: result}

def select_10(student_, tutor_):
    """
    Список курсів, які певному студенту читає певний викладач.
    :return: list[dict]

    SELECT st.name, s.name, t.name
    FROM students AS st, subjects AS s 
    INNER JOIN marks AS m ON m.subject_id= s.id AND st.id = m.student_id
    INNER JOIN tutors AS t ON t.id = s.tutor_id 
    WHERE  st.name = 'Sabrina Wallace' AND t.name = 'John Newton'
    GROUP BY s.name;
    """
    result = session.query(Subject.name) \
        .select_from(Mark).join(Subject).join(Tutor).filter(Tutor.name==tutor_).join(Student).filter(Student.name==student_).group_by(Subject.name).all()

    return {f"student {student_}, tutor {tutor_}": result}

def select_11(student_, tutor_):
    """
    Середній бал, який певний викладач ставить певному студентові.
    :return: list[dict]

    SELECT t.name, AVG(m.mark), st.name  
    FROM marks m
    INNER JOIN students st ON m.student_id = st.id
    INNER JOIN subjects s ON m.subject_id= s.id 
    INNER JOIN tutors t ON s.tutor_id = t.id
    WHERE t.name = "Dylan Holloway" AND st.name = 'Virginia Short'
    GROUP BY st.name;
    """
    result = session.query(Student.name, func.round(func.avg(Mark.mark), 2).label('avg_mark')) \
        .select_from(Mark).join(Subject).join(Student).filter(Student.name==student_).join(Tutor).filter(Tutor.name==tutor_).group_by(Student.name).all()

    return result




def select_12(subject_, group_):

    """

    Оцінки студентів у певній групі з певного предмета на останньому занятті.

    select subj.name as subject, g.number_group , st.name as student, m2.mark , m2.date_ 
    from marks m2 
    inner join students st on m2.student_id = st.id 
    inner join subjects subj on subj.id = m2.subject_id  
    inner join groups g on g.id = st.number_group
    where g.number_group  = 'SA3' and subj.name = 'chemistry'
    and m2.date_=(select MAX(m.date_)
    from marks m 
    inner join students s2 on s2.id  = m.student_id  
    inner join subjects s on s.id = m.subject_id 
    where s.name = 'chemistry')

    """ 

    subquery = (select(func.max(Mark.date_)).join(Student).join(Subject).where(Subject.name == subject_)).scalar_subquery()

    result = session.query(Subject.name,
                    Student.name,
                    Group.number_group,
                    Mark.date_,
                    Mark.mark
                      ) \
        .select_from(Mark) \
        .join(Student) \
        .join(Subject) \
        .join(Group)\
        .filter(and_(Subject.name == subject_, Group.number_group== group_, Mark.date_ == subquery)) \
        .all()
    return result

if __name__ == '__main__':
    print('*1*', select_1())
    print('*2*', select_2('astronomy'))
    print('*3*', select_3('physics'))
    print('*4*', select_4())
    print('*5*', select_5('Dylan Holloway'))
    print('*6*', select_6('GT5'))
    print('*7*', select_7('GT5', 'physics'))
    print('*8*', select_8('Dylan Holloway'))
    print('*9*', select_9('Sabrina Wallace'))
    print('*10*', select_10('Sabrina Wallace', 'John Newton'))
    print('*11*', select_11('Virginia Short', 'Dylan Holloway'))
    print('*12*', select_12('chemistry', 'SA3'))
