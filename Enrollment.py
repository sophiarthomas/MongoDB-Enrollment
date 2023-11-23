import pymongo
from pprint import pprint

def create_enrollment_schema(db):
    enrollment_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': '',
                'required': [],
                'additionalProperties': False,
                'properties': {

                }
            }
        }
    }