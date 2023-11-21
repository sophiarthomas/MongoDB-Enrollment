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



