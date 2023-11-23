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
                    }
                }
            }
         }
    }
    try:
        db.departments = db.create_collection("departments", **department_validator)
        db.departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='departments_name')
        db.departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')
        db.departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_name')
        db. departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,name='departments_office')
    except Exception as e:
        pass
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
            abbreviation = input("Abbreviation (String length 6)--> ")
            chair_name = input("Chair Name (String length 80)--> ")
            building = input("Building (String length 10)--> ")
            office = int(input("Office (Integer)--> "))
            description = input("Description (String length 80)--> ")

            department = {
                "name": name,
                "abbreviation": abbreviation,
                "chair_name": chair_name,
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
    name: str = ''
    while not found:
        name = input("Department's name-->")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": name})
    return found_department


def delete_department(db):
    department = select_department(db)
    departments = db["departments"]
    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments")


def list_department(db):
    departments = db["departments"].find({}).sort("name", pymongo.ASCENDING)
    for department in departments:
        pprint(department)
