import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
import certifi
from menu_definitions import menu_main, add_menu, delete_menu, list_menu
import Department
import Course
import Student
import Section
import Major


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


"""DEPARTMENT"""
def add_department(db):
    Department.add_department(db)
def select_department(db):
    Department.select_department(db)
def delete_department(db):
    Department.delete_department(db)
def list_department(db):
    Department.list_department(db)


"""COURSE"""
def add_course(db):
    Course.add_course(db)
def delete_course(db):
    Course.delete_course(db)
def list_course(db):
    Course.list_course(db)


"""STUDENT"""
def add_student(db):
    Student.add_student(db)
def select_student(db):
    Student.select_student(db)
def delete_student(db):
    Student.delete_student(db)
def list_student(db):
    Student.list_student(db)
def add_major_student(db):
    Student.add_major_student(db)


"""SECTION"""
def add_section(db):
    Section.add_section(db)
def select_section(db):
    Section.select_section(db)
def delete_section(db):
    Section.delete_section(db)
def list_section(db):
    Section.list_section(db)


"""MAJOR"""
def add_major(db):
    Major.add_major(db)
def select_major(db):
    Major.select_major(db)
def delete_major(db):
    Major.delete_major(db)
def list_major(db):
    Major.list_major(db)


def boilerplate(db):
    """
        Add boilerplate data initially to jump start the testing.  Remember that there is no
        checking of this data, so only run this option once from the console, or you will
        get a uniqueness constraint violation from the database.
        :param db:      reference to the database
        :return:        None
        """
    department = {
        "name": 'Engineering',
        "abbreviation": 'ENGR',
        "chair_name": 'Daniel Caesar',
        "building": 'VEC',
        "office": 100,
        "description": 'description of engr'
    }
    course = {
        "department_abbreviation": department.get('abbreviation'),
        "course_name": 'Database',
        "course_number": 323,
        "units": 3,
        "description": 'description of databases'
    }
    section = {
        "department_abbreviation": course.get('department_abbreviation'),
        "course_number": course.get('course_number'),
        "section_number": 1,
        "semester": 'Fall',
        "year": 2023,
        "building": 'ECS',
        "room": 100,
        "schedule": 'MW',
        "instructor": 'David Brown',
        "start_hour": 8,
        "start_minute": 30
    }
    major = {
        "name": 'Computer Science'
    }
    student = {
        "first_name": 'Sophia',
        "last_name": 'Thomas',
        "e_mail": 'sophia@gmail.com'
    }
    db.departments.insert_one(department)
    db.courses.insert_one(course)
    db.sections.insert_one(section)
    db.majors.insert_one(major)
    db.students.insert_one(student)


def clear_documents(db):
    """
    Wipes the collections in the database of all documents
    :param db:
    :return:
    """
    db.departments.delete_many({})
    db.courses.delete_many({})
    db.majors.delete_many({})
    db.students.delete_many({})
    db.sections.delete_many({})


def restart(db):
    """
    Drops and creates each collection, to start fresh
    :param db:
    :return:
    """
    db.departments.drop()
    db.courses.drop()
    db.majors.drop()
    db.students.drop()
    db.sections.drop()
    Department.create_department_schema(db)
    Course.create_course_schema(db)
    Major.create_major_schema(db)
    Student.create_student_schema(db)
    Section.create_section_schema(db)
    print(db.list_collection_names())


def pcoll(banner: str, recs):
    """
    Print out all the documents in recs.
    :param banner:  The prompt that you want displayed to the console.
    :param recs:    The iterable list of records (documents) that you want printed.
    :return:        None
    """
    print(banner)
    for rec in recs:
        pprint(rec)


if __name__ == '__main__':
    cluster = f"mongodb+srv://sophiathomas02:iCjcL1jUWQYLyCjR@cecs-323-fall-2023.ybsdndr.mongodb.net/?retryWrites=true&w=majority"
    # password: str = getpass.getpass('Mongo DB password -->')
    # username: str = input('Database username [CECS-323-Spring-2023-user] -->') or \
    #                 "CECS-323-Spring-2023-user"
    # project: str = input('Mongo project name [cecs-323-spring-2023] -->') or \
    #                "CECS-323-Spring-2023"
    # hash_name: str = input('7-character database hash [puxnikb] -->') or "puxnikb"
    # cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    # print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster, tlsCAFile=certifi.where())
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["SingleCollection"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    Department.create_department_schema(db)
    pprint(db.departments.index_information())

    Course.create_course_schema(db)
    pprint(db.courses.index_information())

    Major.create_major_schema(db)
    pprint(db.majors.index_information())

    Student.create_student_schema(db)
    pprint(db.students.index_information())

    Section.create_section_schema(db)
    pprint(db.sections.index_information())


    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)