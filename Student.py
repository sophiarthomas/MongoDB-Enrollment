import pymongo
from pprint import pprint
from datetime import datetime, timezone
import Major
import Enrollment
import Section

def create_student_schema(db):
	today = datetime.utcnow()
	student_validator={
		 'validator': {
			'$jsonSchema': {
				'bsonType': 'object',
				'description': 'A person attending university to earn a degree or credential',
				'required': ['last_name', 'first_name', 'e_mail'],
				'additionalProperties': False,
				'properties': {
					'_id': {},
					'last_name': {
						'bsonType': 'string',
						'description': 'surname of the student',
						'minLength': 3,
						'maxLength': 80
					},
					'first_name': {
						'bsonType': 'string',
						'description': 'given name of the student',
						'minLength': 3,
						'maxLength': 80
					},
					'e_mail': {
						'bsonType': 'string',
						'description': 'electronic mail address of the student',
						'minLength': 10,
						'maxLength': 255
					},
					'student_major': {
						'bsonType': 'array',
						'description': 'array of majors the student has declared ',
						'items': {
							'bsonType': 'object',
							'properties': {
								'major_name': {
									'bsonType': 'string',
									'description': 'name of the major the student has declared'
								},
								'declaration_date': {
									'bsonType': 'date',
									'description': 'date when the major was declared'
								}
							},
							'additionalProperties':False,
							'required': ['major_name', 'declaration_date']
						},
						'maxItems': 5
					},
					'sections': {
						'bsonType': 'array',
						'description': 'array of sections the student is enrolled in',
						'properties': {
							'section_id': {
								'bsonType': 'objectId',
								'description': 'number that uniquely identifies the section'
							},
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
							'enrollment': Enrollment.enrollmentType
							}
						}
					}
				}
			}
		 }



	# Student is our students collection within this database.
	# Merely referencing this collection will create it, although it won't show up in Atlas until
	# We insert our first document into this collection.
	try:
		db.create_collection("students", **student_validator)
		db.students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
							  unique=True, name="students_last_and_first_names")
		db.students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')
	except Exception as e:
		print(e)
	students = db["students"]
	student_count = students.count_documents({})
	print(f"Students in the collection so far: {student_count}")


def add_student(db):
	"""
	Add a new student, making sure that we don't put in any duplicates,
	based on all the candidate keys (AKA unique indexes) on the
	students collection.  Theoretically, we could query MongoDB to find
	the uniqueness constraints in place, and use that information to
	dynamically decide what searches we need to do to make sure that
	we don't violate any of the uniqueness constraints.  Extra credit anyone?
	:param collection:  The pointer to the students collection.
	:return:            None
	"""
	# Create a "pointer" to the students collection within the db database.
	collection = db["students"]

	while True:
		try:
			lastName = input("Student last name--> ")
			firstName = input("Student first name--> ")
			email = input("Student e-mail address--> ")

			student = {
				"last_name": lastName,
				"first_name": firstName,
				"e_mail": email
			}

			collection.insert_one(student)
			print("Student added successfully.")
			break
		except Exception as e:
			print("An error occurred:", str(e))
			print("Please re-enter student information.")


def select_student(db):
	"""
	Select a student by the combination of the last and first.
	:param db:      The connection to the database.
	:return:        The selected student as a dict.  This is not the same as it was
					in SQLAlchemy, it is just a copy of the Student document from
					the database.
	"""
	# Create a connection to the students collection from this database
	collection = db["students"]
	found: bool = False
	lastName: str = ''
	firstName: str = ''
	while not found:
		lastName = input("Student's last name--> ")
		firstName = input("Student's first name--> ")
		name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
		found = name_count == 1
		if not found:
			print("No student found by that name.  Try again.")
	found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
	return found_student


def delete_student(db):
	"""
	Delete a student from the database.
	:param db:  The current database connection.
	:return:    None
	"""
	# student isn't a Student object (we have no such thing in this application)
	# rather it's a dict with all the content of the selected student, including
	# the MongoDB-supplied _id column which is a built-in surrogate.
	student = select_student(db)
	# Create a "pointer" to the students collection within the db database.
	students = db["students"]
	# student["_id"] returns the _id value from the selected student document.
	deleted = students.delete_one({"_id": student["_id"]})
	# The deleted variable is a document that tells us, among other things, how
	# many documents we deleted.
	print(f"We just deleted: {deleted.deleted_count} students.")


def list_student(db):
	"""
	List all of the students, sorted by last name first, then the first name.
	:param db:  The current connection to the MongoDB database.
	:return:    None
	"""
	# No real point in creating a pointer to the collection, I'm only using it
	# once in here.  The {} inside the find simply tells the find that I have
	# no criteria.  Essentially this is analogous to a SQL find * from students.
	# Each tuple in the sort specification has the name of the field, followed
	# by the specification of ascending versus descending.
	students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
											 ("first_name", pymongo.ASCENDING)])
	# pretty print is good enough for this work.  It doesn't have to win a beauty contest.
	for student in students:
		pprint(student)


def add_major_student(db):
	"""
	from what i can tell this function will override the last major declaration
	if the student and major are the same, but a check should be made before students.update_one
	is written
	"""
	students = db["students"]
	student = select_student(db)

	try:
		major = Major.select_major(db)

		# check if the entered major and student combination are already declared
		major_check = major.get("name")
		existing_majors = []
		for m in student.get("student_major", []):
			existing_majors.append(m.get("major_name"))
		if major_check in existing_majors:
			print(f"Student has already declared {major_check} as a major.")
			return

		declarationDate = datetime.utcnow()

		studentMajor = {
			"major_name": major.get("name"),
			"declaration_date": declarationDate
		}
		students.update_one(
			{"_id": student.get("_id")},
			{"$push": {"student_major": studentMajor}}
		)
		print("Student Major added successfully")
	except Exception as e:
		print(e)


def select_major_student(db):
	collection = db["students"]
	found: bool = False
	#selecting a student
	student = select_student(db)
	while not found:
		#selecting a major
		major = Major.select_major(db)
		#counting how many majors match the entered information
		student_major_count: int = collection.count_documents({"_id": student.get("_id"),
															   "student_major":  {"$elemMatch": {"major_name": major.get("name")}}})
		found = student_major_count == 1
		if not found:
			print("No student major found by that pair of student and major. Try again.")
	#finding the student with the matching major
	found_student = collection.find_one({"_id": student.get("_id"),
										 "student_major": {"$elemMatch": {"major_name": major.get("name")}}})
	return found_student


def delete_major_student(db):
	student_major = select_major_student(db)
	if student_major:
		student_id = student_major["_id"]
		major_name = student_major["student_major"][0]["major_name"]
		db.students.update_one(
			{"_id": student_id},
			{"$pull": {"student_major": {"major_name": major_name}}}
		)
		print("Student major deleted successfully")



def list_student_major(db):
	students = db["students"]
	all_students = students.find({})
	for student in all_students:
		criteria = {
			'first_name': student.get('first_name'),
			'last_name': student.get('last_name')
		}
		projection = {
			'_id': 0,
			'e_mail':0,
			'sections':0,
			'student_major':0
		}
		result = students.find_one(criteria, projection)

		majors = student.get('student_major', [])
		if majors:
			pprint(result)
			for major in majors:
				pprint(major)

def add_section_student(db):
	students = db["students"]
	sections = db["sections"]
	student = select_student(db)
	enrollment = {}
	while True:
		try:
			section = Section.select_section(db)
			enrollment_type = input("Enter PassFail or LetterGrade (P/L)--> ")
			if enrollment_type.lower() == "p":
				applicationDate = datetime.utcnow()
				enrollment = {'application_date': applicationDate}
			elif enrollment_type.lower() == 'l':
				minSatisfactory = input("Enter the Minimum Satisfactory Grade (A, B, C)--> ")
				enrollment = {'min_satisfactory': minSatisfactory}

			section_info = {
				"section_id": section.get("_id"),
				"department_abbreviation": section.get("department_abbreviation"),
				"course_number": section.get("course_number"),
				"section_number": section.get("section_number"),
				"semester": section.get("semester"),
				"year": section.get("year"),
				"enrollment": {"enrollment_type": enrollment}
			}
			students.update_one(
				{"_id": student.get("_id")},
				{"$push": {"sections": section_info}}
			)

			enrollment = {
				"student_id": student.get("_id"),
				"enrollment_type": enrollment
			}
			sections.update_one(
				{"_id": section.get("_id")},
				{"$push": {"enrollments": enrollment}}
			)
			print("Student Section added successfully")
			break
		except Exception as e:
			print(e)
