import pymongo
from pprint import pprint

def create_student_schema(db):
	student_validator={
		 'validator': {
			'$jsonSchema': {
				'bsonType': "object",
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
							  unique=True,
							  name="students_last_and_first_names")
		db.students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')
	except Exception as e:
		pass
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
	unique_name: bool = False
	unique_email: bool = False
	lastName: str = ''
	firstName: str = ''
	email: str = ''
	while not unique_name or not unique_email:
		lastName = input("Student last name--> ")
		firstName = input("Student first name--> ")
		email = input("Student e-mail address--> ")
		name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
		unique_name = name_count == 0
		if not unique_name:
			print("We already have a student by that name.  Try again.")
		if unique_name:
			email_count = collection.count_documents({"e_mail": email})
			unique_email = email_count == 0
			if not unique_email:
				print("We already have a student with that e-mail address.  Try again.")
	# Build a new students document preparatory to storing it
	student = {
		"last_name": lastName,
		"first_name": firstName,
		"e_mail": email
	}
	results = collection.insert_one(student)


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
