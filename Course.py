import pymongo
from pprint import pprint
import Department

def create_course_schema(db):
    course_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A catalog entry. Each course proposes to offer students who enroll in \
                a section of the course an organized sequence of lessons and assignments aimed at teaching \
                them specified skills.',
                'required': ['department_abbreviation', 'course_name', 'course_number', 'units', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'department_abbreviation': {
                        'bsonType': 'string',
                        'description': 'embedded department abbreviation the course falls under',
                        'maxLength': 6
                    },
                    'course_name': {
                        'bsonType': 'string',
                        'description': 'A text string that identifies the course',
                    },
                    'course_number': {
                        'bsonType': 'int',
                        'description': 'Numerical value that correlates with the course name',
                        'minimum': 100,
                        'maximum': 699
                    },
                    'units': {
                        'bsonType': 'int',
                        'description': 'The measure of the amount of work required to complete a course',
                        'minimum': 1,
                        'maximum': 5,
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': 'Provides additional information about the course',
                    },
                    'sections': {
                        'bsonType': 'array',
                        'description': 'array of sections taught for a course',
                        'additionalItems': False,
                        'items': {
                            'bsonType': 'object',
                            'required': ['section_id', 'section_number', 'semester', 'year'],
                            'additionalProperties': False,
                            'properties': {
                                'section_id': {
                                    'bsonType': 'objectId',
                                    'description': 'Uniquely identifies a section'
                                },
                                'section_number': {
                                    'bsonType': 'int',
                                    'description': 'Two-digit numerical value that correlates to the section',
                                    'minimum': 1
                                },
                                'semester': {
                                    'bsonType': 'string',
                                    'description': 'Time of year that the section takes place',
                                    'enum': ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
                                },
                                'year': {
                                    'bsonType': 'int',
                                    'description': 'year that the section takes place',
                                    "minimum": 1949,
                                    'maximum': 2023
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    try:
        db.create_collection("courses", **course_validator)
        db.courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING)],
                                unique=True, name='courses_department_abbreviation_number')
        db.courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_name', pymongo.ASCENDING)],
                                unique=True, name='courses_department_abbreviation_name')
    except Exception as e:
        print(e)
    courses = db["courses"]
    course_count = courses.count_documents({})
    print(f"Courses in the collection so far {course_count}")


def add_course(db):
    collection = db["courses"]
    department = Department.select_department(db)

    while True:
        try:
            courseName = input("Course Name--> ")
            courseNumber = int(input("Course Number (100-699) --> "))
            units = int(input("Course Units (1-5) --> "))
            description = input("Course Description--> ")

            course = {
                "department_abbreviation": department.get("abbreviation"),
                "course_name": courseName,
                "course_number": courseNumber,
                "units": units,
                "description": description
            }
            collection.insert_one(course)

            #Adds course reference and denormalized values(course_number&course_name) to 'courses' array in departments
            courses = {
                "course_id": course.get("_id"),
                "course_number": courseNumber,
                "course_name": courseName
            }
            db.departments.update_one(
                {"_id": department.get("_id")},
                {"$push": {"courses": courses}}
            )
            print("Course added successfully.")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            print("Please re-enter course information.")


def select_course(db):
    collection = db["courses"]
    department = Department.select_department(db)
    found: bool = False
    courseNumber: int = 0

    while not found:
        courseNumber = int(input("Course Number--> "))
        course_count: int = collection.count_documents({"department_abbreviation": department.get("abbreviation"),
                                                        "course_number": courseNumber})
        found = course_count == 1
        if not found:
            print("No course found by that department and course number. Try again.")
    found_course = collection.find_one({"department_abbreviation": department.get("abbreviation"), "course_number": courseNumber})
    return found_course


def delete_course(db):
    collection = db["courses"]
    course = select_course(db)
    section_count = len(course.get("sections", []))
    if section_count == 0:
        db.departments.update_one(
            {"abbreviation": course.get("department_abbreviation")},
            {"$pull" : {"courses": {"course_id": course.get("_id")}}}
        )
        deleted = collection.delete_one({"_id": course["_id"]})
        print(f"We just deleted: {deleted.deleted_count} course")
    else:
        print(f"There are {section_count} sections for that course. Delete them first, "
              f"then come back here to delete the course.")


def list_course(db):
    courses = db["courses"].find({}).sort("course_number", pymongo.ASCENDING)
    for course in courses:
        pprint(course)