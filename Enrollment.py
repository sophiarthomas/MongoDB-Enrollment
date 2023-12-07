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


enrollmentSchema = {
    'bsonType': 'array',
    'description': 'enrollment information between student and section, containing enrollment_type',
    'items': {
        'bsonType': 'object',
        'required': ['student_id', 'enrollment_type'],
        'additionalProperties': False,
        'properties': {
            'student_id': {
                'bsonType': 'objectId',
                'description': '_id of the student enrolled'
            },
            'enrollment_type': enrollmentType
        }
    }

}

