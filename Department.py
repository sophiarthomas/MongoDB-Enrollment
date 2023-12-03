import pymongo
from pprint import pprint

def create_department_schema(db):
    department_validator={
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "An 4 year establishment that issues degrees to students who have completed their education",
                'required': ['name', 'abbreviation', 'chair_name', 'building', 'office', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'name': {
                        'bsonType': 'string',
                        'description': 'name of the department',
                        'minLength': 10,
                        'maxLength': 50
                    },
                    'abbreviation': {
                        'bsonType': 'string',
                        'description': 'shortened identifiable name of the department',
                        'maxLength': 6
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'description': 'name of the department chair',
                        'maxLength': 80
                    },
                    'building': {
                        'bsonType': 'string',
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        'description': 'name of building where the department office resides',
                        'maxLength': 10
                    },
                    'office': {
                        'bsonType': 'int',
                        'description': 'room number of the department office',
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': '',
                        'minLength': 10,
                        'maxLength': 80
                    },
                    'courses': {
                        'bsonType': 'array',
                        'description': 'array of courses offered by the department',
                        'additionalItems': False,
                        'items': {
                            'bsonType': 'object',
                            'properties': {
                                'course_id': {
                                    'bsonType': 'objectId',
                                    'description': 'digits that uniquely identify a course'
                                },
                                'course_number': {
                                    'bsonType': 'int',
                                    'description': 'Numerical value that correlates with the course name',
                                    'minimum': 100,
                                    'maximum': 699
                                },
                                'course_name': {
                                    'bsonType': 'string',
                                    'description': 'A text string that identifies the course',
                                }
                            }
                        }
                    },
                    'majors': {
                        'bsonType': 'array',
                        'description': 'array of majors offered by the department',
                        'additionalItems': False,
                        'items': {
                            'bsonType': 'object',
                            'required': ['major_id', 'major_name'],
                            'additionalProperties': False,
                            'properties': {
                                'major_id': {
                                    'bsonType': 'objectId',
                                },
                                'major_name': {
                                    'bsonType': 'string',
                                    'description': 'a text string that identifies the major'
                                }
                            }
                        }
                    }
                }
            }
         }
    }
    try:
        db.create_collection("departments", **department_validator)
        db.departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='departments_name')
        db.departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')
        db.departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_name')
        db. departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,name='departments_office')
    except Exception as e:
        print(e)
    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")


def add_department(db):
    """
    Add a new department, making sure that we don't put in any duplicates,
    based on the department name.
    :param db:  The connection to the current database.
    :return:    None
    """
    collection = db["departments"]

    while True:
        try:
            name = input("Department name (String length 50)--> ")
            abbreviation = input("Department Abbreviation (String length 6)--> ")
            chairName = input("Department Chair Name (String length 80)--> ")
            building = input("Department Building (String length 10)--> ")
            office = int(input("Department Office (Integer)--> "))
            description = input("Department Description (String length 80)--> ")

            department = {
                "name": name,
                "abbreviation": abbreviation,
                "chair_name": chairName,
                "building": building,
                "office": office,
                "description": description
            }
            collection.insert_one(department)
            print("Department added successfully.")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            print("Please re-enter department information.")


def select_department(db):
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Department's abbreviation-->")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department found by that abbreviation. Try again.")
    found_department = collection.find_one({"abbreviation": abbreviation})
    return found_department


def delete_department(db):
    collection = db["departments"]
    department = select_department(db)
    #check if there are any courses in the department
    courses_count = len(department.get("courses", []))
    majors_count = len(department.get("majors", []))
    if courses_count == 0 & majors_count == 0:
        deleted = collection.delete_one({"_id": department["_id"]})
        print(f"We just deleted: {deleted.deleted_count} departments")

    else:
        print(f"There are {courses_count} courses and {majors_count} majors in that department. Delete them first, "
              f"then come back here to delete the department.")



def list_department(db):
    departments = db["departments"].find({}).sort("name", pymongo.ASCENDING)
    for department in departments:
        pprint(department)