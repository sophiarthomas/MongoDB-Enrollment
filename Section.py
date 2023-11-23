import pymongo
from pprint import pprint
from datetime import time

#write description for each field
def create_section_schema(db):
    section_validator={
         'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': '',
                'required': ['semester', 'year', 'building', 'room', 'schedule', 'instructor', 'startTime'],
                'additionalProperties': True,
                'properties': {
                #embedded is courseNumber, departmentAbbreviation from courses
                    'id_': {}, #section_number?
                    #'course_number': {"$ref": ""},
                    #'department_abbreviation': {"$ref": ""}, #
                    'semester': {
                        'bsonType': 'string',
                        'description': 'time of year that the section takes place ',
                        'enum': ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
                    },
                    'year': {
                        'bsonType': 'int',
                        'description': 'year that the section takes place '
                        # ensure the year is not before the current year
                    },
                    'building': {
                        'bsonType': 'string',
                        'description': 'name of the building where the course section resides',
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET',
                                 'HSCI', 'NUR', 'VEC']
                    },
                    'room': {
                        'bsonType': 'int',
                        'description': 'room number of the section',
                        'minimum': 1,
                        'maximum': 999
                    },
                    'schedule': {
                        'bsonType': 'string',
                        'description': 'days of the week the section is to take place',
                        'enum': ['MW', 'TuTh', 'MWF', 'F', 'S']
                    },
                    'instructor': {
                        'bsonType': "string",
                        'description': 'staff member teaching the section'
                    },
                    'start_time': {
                        'bsonType': 'time',
                        'description': 'hour and minute of when the section commences'
                        #startTime >= 8:00AM and <= 7:30PM
                    }
                }
            }
         }
    }
    try:
        db.create_collection("sections", **section_validator)
    except Exception as e:
        pass
    sections = db["sections"]
    section_count = sections.count_documents({})
    print(f"Sections in the collection so far: {section_count}")


#to make sure this can work we will have to import something from course
#to get the course number and department abbreviation

def add_section(db):
    collection = db["sections"]

    semester = input("Section semester--> ")
    schedule = input("Section schedule--> ")
    year = int(input("Section year--> "))
    room = int(input("Section room--> "))
    building = input("Section building--> ")
    instructor = input("Section instructor-->")
    start_hour = int(input('Start hour --> '))
    start_minute = int(input('Start minute --> '))
    startTime = time(start_hour, start_minute)

    indexes = collection.list_indexes()
    uniqueness_constraints = [
        index["key"] for index in indexes if index.get("unique", False)
    ]
    for constraint in uniqueness_constraints:
        query = {key: collection[key] for key in constraint}
        if collection.find_one(query):
            print("This section already exists")
        else:
            section = {
                "semester": semester,
                "schedule": schedule,
                "year": year,
                "room": room,
                "building": building,
                "instructor": instructor,
                "start_time": startTime
            }
            results = collection.insert_one(section)


def select_section(db):
    collection = db["sections"]
    found: bool = False
    semester: str = ''
    schedule: str = ''
    year: int = 0
    instructor: str = ''
    startTime: time
    #choose a unique index to find a given section
    while not found:
        semester = input("Section semester--> ")
        schedule = input("Section schedule--> ")
        year = int(input("Section year--> "))
        instructor = input("Section instructor-->")
        start_hour = int(input('Start hour --> '))
        start_minute = int(input('Start minute --> '))
        startTime = time(start_hour, start_minute)
        section_count: int = collection.count_documents({"semester": semester, "schedule": schedule, "year": year,
                                                         "instructor": instructor, "start_time": startTime})
        found = section_count == 1
        if not found:
            print("No section found by the given attributes. Try again")
    found_student = collection.find_one({"semester": semester, "schedule": schedule, "year": year,
                                                         "instructor": instructor, "start_time": startTime})
    return found_student


def delete_section(db):
    section = select_section(db)
    sections = db["sections"]
    deleted = sections.delete_one({"_id": section["_id"]})
    print(f"We just deleted: {deleted.deleted_count} sections")


def list_section(db):
    sections = db["sections"].find({}).sort("_id", pymongo.ASCENDING)
    for section in sections:
        pprint(section)