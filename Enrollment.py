#enrollment embedded into sections

enrollmentType = {
    'oneOf': [
        {
            'bsonType': 'object',
            'required': ['application_date'],
            'additionalProperties': False,
            'properties': {
                'application_date': {
                    'bsonType': 'date',
                    'description': 'the year, month, and day a student applied for passfail '
                }
            }
        },
        {
            'bsonType': 'object',
            'required': ['min_satisfactory'],
            'additionalProperties': False,
            'properties': {
                'min_satisfactory': {
                    'bsonType': 'string',
                    'enum': ['A', 'B', 'C'],
                    'description': 'the minimum grade required for the student to pass the course'
                }
            }
        }
    ]
}
students = { #list of references to students enrolled in given section
    'bsonType': 'object',
    'required': ['student_id'],
    'additionalProperties': False,
    'properties': {
        'student_id': {
            'bsonType': 'objectId',
            'description': '_id of the student enrolled'
        }
    }
}

enrollmentSchema = {
    'bsonType': "object",
    'description': '',
    'required': ['students', 'enrollment_data'],
    'additionalProperties': False,
    'properties': {
        'students': students,
        'enrollment_data': enrollmentType
    }
}

