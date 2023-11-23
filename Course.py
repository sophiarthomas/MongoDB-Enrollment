import pymongo
from pprint import pprint

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


def add_course(db):
    pass


def select_course(db):
    pass


def delete_course(db):
    pass


def list_course(db):
    pass
