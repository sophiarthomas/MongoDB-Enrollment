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
                'required': ['course_name', 'course_number', 'units', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'department_abbreviation': {
                        'bsonType': 'string',
                        'description': 'embedded department abbreviation the course falls under',
                    },
                    'course_name': {
                        'bsonType': 'string',
                        'description': 'A text string that identifies the course',
                    },
                    'course_number': {
                        'bsonType': 'int',
                        'description': 'Numerical value that correlates with the course name',
                        'minLength': 100,
                        'maxLength': 699,
                    },
                    'units': {
                        'bsonType': 'int',
                        'description': 'The measure of the amount of work required to complete a course',
                        'minLength': 1,
                        'maxLength': 5,
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': 'Provides additional information about the course',
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
        pass
    courses = db["courses"]
    course_count = courses.count_documents({})
    print(f"Courses in the collection so far {course_count}")


def add_course(db):
    collection = db["courses"]
    department = Department.select_department(db)

    while True:
        try:
            courseName = input("Course Name--> ")
            courseNumber = int(input("Course Number--> "))
            units = int(input("Course Units--> "))
            description = input("Course Description--> ")

            course = {
                "department_abbreviation": department.get("abbreviation"),
                "course_name": courseName,
                "course_number": courseNumber,
                "units": units,
                "description": description
            }
            collection.insert_one(course)
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
    course = select_course(db)
    if course is None:
        print("Course does not exist. Try again.")
        return
    courses = db["courses"]
    deleted = courses.delete_one({"_id": course["_id"]})
    print(f"We just deleted: {deleted.deleted_count} course")


def list_course(db):
    courses = db["courses"].find({}).sort("course_number", pymongo.ASCENDING)
    for course in courses:
        pprint(course)