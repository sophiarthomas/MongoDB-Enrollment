import pymongo
from pprint import pprint
import Course
import Enrollment

def create_section_schema(db):
    section_validator = {
         'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': 'an instance of a course being taught',
                'required': ['department_abbreviation', 'course_number', 'semester', 'year', 'building',
                             'room', 'schedule', 'instructor', 'start_hour', 'start_minute'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'department_abbreviation': {
                        'bsonType': 'string',
                        'description': 'The name of the department.'
                    },
                    'course_number': {
                        'bsonType': 'int',
                        'description': 'A 3-digit number designating a specific course within a department.'
                    },
                    'section_number': {
                        'bsonType': 'int',
                        'description': 'A 2-digit number designating a section offered of a course during a semester.',
                        'minimum': 1
                    },
                    'semester': {
                        'bsonType': 'string',
                        'description': 'time of year that the section takes place ',
                        'enum': ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
                    },
                    'year': {
                        'bsonType': 'int',
                        'description': 'year that the section takes place',
                        "minimum": 1949,
                        'maximum': 2023
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
                    'start_hour': {
                        'bsonType': "int",
                        "description": "The hour when the section starts.",
                        "minimum": 8,
                        "maximum": 18
                    },
                    'start_minute': {
                        'bsonType': "int",
                        'description': "The minutes into the start_hour when the section starts.",
                        'enum': [0, 30],
                    },
                    'enrollments': Enrollment.enrollmentSchema
                }
            }
         }
    }
    try:
        db.create_collection("sections", **section_validator)
        db.sections.create_index([('course_number', pymongo.ASCENDING), ('section_number', pymongo.ASCENDING),
                                  ('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING)],
                                 unique=True, name="sections_course_number_section_number_semester_year")
        db.sections.create_index([('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING),
                                  ('building', pymongo.ASCENDING), ('room', pymongo.ASCENDING),
                                  ('schedule', pymongo.ASCENDING), ('start_hour', pymongo.ASCENDING),
                                  ('start_minute', pymongo.ASCENDING)],
                                 unique=True, name="sections_semester_year_room_schedule_time")
        db.sections.create_index([('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING),
                                  ('schedule', pymongo.ASCENDING), ('start_hour', pymongo.ASCENDING),
                                  ('start_minute', pymongo.ASCENDING), ('instructor', pymongo.ASCENDING)],
                                 unique=True, name="sections_semester_year_schedule_time_instructor")
        db.sections.create_index([('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING),
                                  ('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING),
                                  ('enrollments.students.student_id', pymongo.ASCENDING)],
                                 unique=True, name="sections_semester_year_department_course_studentID")
    except Exception as e:
        print(e)
    sections = db["sections"]
    section_count = sections.count_documents({})
    print(f"Sections in the collection so far: {section_count}")


def add_section(db):
    collection = db["sections"]
    course = Course.select_course(db)
    while True:
        try:
            sectionNumber = int(input ("Section number--> "))
            semester = input("Section semester--> ")
            schedule = input("Section schedule--> ")
            year = int(input("Section year--> "))
            room = int(input("Section room--> "))
            building = input("Section building--> ")
            instructor = input("Section instructor-->")
            startHour = input("Start Hour--> ")
            startMinute = input("Start Minute--> ")

            section = {
                "department_abbreviation": course.get("department_abbreviation"),
                "course_number": course.get("course_number"),
                "section_number": sectionNumber,
                "semester": semester,
                "schedule": schedule,
                "year": year,
                "room": room,
                "building": building,
                "instructor": instructor,
                "start_hour": startHour,
                "start_minute": startMinute
            }
            collection.insert_one(section)
            print("Section added successfully.")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            print("Please re-enter section information.")


def select_section(db):
    collection = db["sections"]
    course = Course.select_course(db)
    found: bool = False
    sectionNumber: int = 0
    semester: str = ''
    year: int = 0

    while not found:
        sectionNumber = int(input("Section Number--> "))
        semester = input("Section Semester--> ")
        year = int(input("Section Year--> "))
        section_count: int = collection.count_documents({"course_number": course.get("course_number"),
                                                         "section_number": sectionNumber,
                                                         "semester": semester,
                                                         "year": year})
        found = section_count == 1
        if not found:
            print("No section found by the given attributes. Try again")
    found_student = collection.find_one({"course_number": course.get("course_number"),
                                                         "section_number": sectionNumber,
                                                         "semester": semester,
                                                         "year": year})
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