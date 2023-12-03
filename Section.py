import pymongo
from pprint import pprint
import Course
import Enrollment
import Student
from datetime import datetime, timezone, date


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
        #issue when adding a new section, student_id takes on null value
        # db.sections.create_index([('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING),
        #                           ('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING),
        #                           ('enrollments.student_id', pymongo.ASCENDING)],
        #                          unique=True, sparse=True, name="sections_semester_year_department_course_studentId")
    except Exception as e:
        pass
    sections = db["sections"]
    section_count = sections.count_documents({})
    print(f"Sections in the collection so far: {section_count}")


def add_section_to_course(db, course, section):
    sec = {
        'section_id': section.get("_id"),
        'section_number': section.get("section_number"),
        'semester': section.get("semester"),
        'year': section.get("year")
    }
    db.courses.update_one(
        {"_id": course.get("_id")},
        {"$push": {"sections": sec}}
    )


def add_section(db):
    sections = db["sections"]
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
            startHour = int(input("Start Hour--> "))
            startMinute = int(input("Start Minute--> "))

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
            #Adding a new section document to the section collection
            result = sections.insert_one(section)

            #Adding section information to the sections array in courses
            add_section_to_course(db, course, section)

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
    sections = db["sections"]
    section = select_section(db)
    #ensure that there are no enrollments before deleting
    enrollment_count: int = sections.count_documents({"_id": section.get("_id"),
                                                        "enrollments": {"$exists": True, "$ne": []}})
    if enrollment_count == 0:
        #removing section from the array sections within course
        db.courses.update_one(
            {"department_abbreviation": section.get("department_abbreviation"),
             "course_number": section.get("course_number")},
            {"$pull": {"sections": {"section_id": section.get("_id")}}}
        )
        #delete section document from section collection
        deleted = db.sections.delete_one({"_id": section["_id"]})
        print(f"We just deleted: {deleted.deleted_count} sections")
    else:
        print(f"There are {enrollment_count} student(s) enrolled in this section. \n"
              f"You must delete all enrollments before deleting this section.")


def list_section(db):
    sections = db["sections"].find({}).sort("_id", pymongo.ASCENDING)
    for section in sections:
        pprint(section)


############### Enrollment Functions ###############

def add_student_section(db):
    """
    Adding a student and enrollment_type to the enrollments array in sections
    Adding section and enrollment information to the sections array in students
    to represent an enrollment
    :param db:
    :return:
    """
    print("adding a student to a section ")
    sections = db["sections"]
    students = db["students"]
    section = select_section(db)
    enrollment = {}
    enrollment_type = {}
    while True:
        student = Student.select_student(db)
        exists = sections.find_one({
            "semester": section.get("semester"),
            "year": section.get("year"),
            "department_abbreviation": section.get("department_abbreviation"),
            "course_number": section.get("course_number"),
            "enrollments.student_id": student.get("_id")
        }
        )
        if not exists:
            try:
                enrollmentType = input("Enter PassFail or LetterGrade (P/L)--> ")
                if enrollmentType.lower() == "p":
                    applicationDate = datetime.utcnow()
                    enrollment = {
                        'student_id': student.get("_id"),
                        'enrollment_type': {'application_date': applicationDate}
                    }
                    enrollment_type = {"application_date": applicationDate}
                elif enrollmentType.lower() == "l":
                    minSatisfactory = input("Enter the Minimum Satisfactory Grade (A, B, C)--> ")
                    enrollment = {
                        'student_id': student.get("_id"),
                        'enrollment_type': {'min_satisfactory': minSatisfactory}
                    }
                    enrollment_type = minSatisfactory
                studentEnrollment = {
                    'section_id': section.get("_id"),
                    'department_abbreviation': section.get("department_abbreviation"),
                    'course_number': section.get("course_number"),
                    'section_number': section.get("section_number"),
                    'semester': section.get("semester"),
                    'year': section.get("year"),
                    'enrollment': enrollment_type
                }
                sections.update_one(
                    {"_id": section.get("_id")},
                    {"$push": {"enrollments": enrollment}}
                )
                students.update_one(
                    {"_id": student.get("_id")},
                    {"$push": {"sections": studentEnrollment}}
                )
                print("Enrollment added successfully")
                break
            except Exception as e:
                pprint(e)
        else:
            print("That student is already enrolled in a section of the same course during the same semester. Try again.")



def select_student_section(db):
    collection = db["sections"]
    found: bool = False
    #selecting a section
    section = select_section(db)

    while not found:
        #selecting a student
        student = Student.select_student(db)
        #counting how many enrollment documents match the entered information
        enrollment_count: int = collection.count_documents({"_id": section.get("_id"),
                                                            "enrollments": {"student_id": student.get("_id")}})
        found = enrollment_count == 1
        if not found:
            print("No enrollment found by that pair of section and student. Try again")
    #finding the section with the matching enrollment
    found_enrollment_section = collection.find_one({"_id": section.get("_id"),
                                            "enrollments": {"student_id": student.get("_id")}})
    return found_enrollment_section


def delete_student_section(db):
    enrollment_section = select_student_section(db)
    if enrollment_section:
        section_id = enrollment_section["_id"]
        student_id = enrollment_section["enrollments"][0]["student_id"]
        #deleting enrollments from section document
        db.sections.update_one(
            {"_id": section_id},
            {"$pull": {"enrollments": {"student_id": student_id}}}
        )
        #deleting denormalized section information from students
        db.students.update_one(
            {"_id": student_id},
            {"$pull": {"sections": {"section_id": section_id}}}
        )
        print("Enrollment deleted successfully.")
    else:
        print("No enrollment found.")


def list_enrollment(db):
    all_sections = db.sections.find({})
    for section in all_sections:
        criteria = {
            'department_abbreviation': section.get('department_abbreviation', ''),
            'course_number': section.get('course_number', ''),
            'section_number':  section.get('section_number', ''),
            'year': section.get('year', '')
        }
        projection = {
            'building': 0,
            'room': 0,
            'schedule': 0,
            'instructor': 0,
            'start_hour': 0,
            'start_minute': 0,
            'enrollments': 0
        }
        result = db.sections.find_one(criteria, projection)

        enrollments = section.get('enrollments', [])
        if enrollments:
            pprint(result)
            for enrollment in enrollments:
                pprint(enrollment)