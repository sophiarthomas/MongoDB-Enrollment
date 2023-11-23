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


#DEPARTMENT
def add_department(db):
    Department.add_department(db)
def select_department(db):
    Department.select_department(db)
def delete_department(db):
    Department.delete_department(db)
def list_department(db):
    Department.list_department(db)


#COURSE
def add_course(db):
    Course.add_course(db)
def delete_course(db):
    Course.delete_course(db)
def list_course(db):
    Course.list_course(db)


#STUDENT
def add_student(db):
    Student.add_student(db)
def select_student(db):
    Student.select_student(db)
def delete_student(db):
    Student.delete_student(db)
def list_student(db):
    Student.list_student(db)


#SECTION
def add_section(db):
    Section.add_section(db)
def select_section(db):
    Section.select_section(db)
def delete_section(db):
    Section.delete_section(db)
def list_section(db):
    Section.list_section(db)


#MAJOR
def add_major(db):
    Major.add_major(db)
def select_major(db):
    Major.select_major(db)
def delete_major(db):
    Major.delete_major(db)
def list_major(db):
    Major.list_major(db)

#COURSE
#STUDENT
#ENROLLMENT
#STUDENTMAJOR



if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [CECS-323-Spring-2023-user] -->') or \
                    "CECS-323-Spring-2023-user"
    project: str = input('Mongo project name [cecs-323-spring-2023] -->') or \
                   "CECS-323-Spring-2023"
    hash_name: str = input('7-character database hash [puxnikb] -->') or "puxnikb"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster, tlsCAFile=certifi.where())
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["SingleCollection"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())


    Department.create_department_schema(db)
    Course.create_course_schema(db)
    Major.create_major_schema(db)
    Student.create_student_schema(db)
    Section.create_section_schema(db)


    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
