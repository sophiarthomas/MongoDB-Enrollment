import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
import certifi
from menu_definitions import menu_main, add_menu, delete_menu, list_menu
import DepartmentCollection
import StudentCollection
import DepartmentSchema
import StudentSchema


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
    DepartmentCollection.add_department(db)

def select_department(db):
    DepartmentCollection.select_department(db)

def delete_department(db):
    DepartmentCollection.delete_department(db)

def list_department(db):
    DepartmentCollection.list_department(db)


#STUDENT
def add_student(db):
    StudentCollection.add_student(db)

def select_student(db):
    StudentCollection.select_student(db)

def delete_student(db):
    StudentCollection.delete_student(db)

def list_student(db):
    StudentCollection.list_student(db)


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

    # Student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # We insert our first document into this collection.
    students = db["students"]
    try:
        students = db.create_collection("students", **StudentSchema.student_validator)
    except Exception as e:
        pass
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")


    departments = db["departments"]
    try:
        departments = db.create_collection("departments", **DepartmentSchema.department_validator)
    except Exception as e:
        pass
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")


    # ************************** Set up the students collection unique index
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        pass
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        pass
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')
    # pprint(students.index_information())


    # ************************* Set up departments collection unique index
    departments_indexes = departments.index_information()
    if 'departments_name' in departments_indexes.keys():
        pass
    else:
         # Create a single UNIQUE index on just the name
        departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='departments_name')
    if 'departments_abbreviation' in departments_indexes.keys():
        pass
    else:
        #Create a single UNIQUE index on just the abbreviation
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')
    if 'departments_chair_name' in departments_indexes.keys():
        pass
    else:
        #Create a single UNIQUE index on just the chair
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_name')
    if 'departments_office' in departments_indexes.keys():
        pass
    else:
        #Create a single UNIQUE index on BOTH the building and office
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,
                                 name='departments_office')

    # pprint(departments.index_information())


    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)