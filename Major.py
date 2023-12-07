import pymongo
from pprint import pprint
import Department

def create_major_schema(db):
	major_validator={
		 'validator': {
			'$jsonSchema': {
				'bsonType': "object",
				'description': 'A specific area of study in which a student chooses to specialize',
				'required': ['department_abbreviation', 'name'],
				'additionalProperties': False,
				'properties': {
					'_id': {},
					'department_abbreviation': {
						'bsonType': 'string',
						'description': 'shortened identifiable name of the department',
						'maxLength': 6
					},
					'name': {
						'bsonType': 'string',
						'description': 'a text string that identifies the major'
					}
				}
			}
		 }
	}
	try:
		db.create_collection("majors", **major_validator)
		db.majors.create_index([("name", pymongo.ASCENDING)], unique=True)
	except Exception as e:
		pass

	majors = db["majors"]
	major_count = majors.count_documents({})
	print(f"Majors in the collection so far: {major_count}")


def add_major(db):
	collection = db["majors"]
	department = Department.select_department(db)
	while True:
		try:
			name = input("Major name--> ")

			major = {
				"department_abbreviation": department.get("abbreviation"),
				"name": name
			}
			collection.insert_one(major)
			db.departments.update_one(
				{"_id": department.get("_id")},
				{"$push": {"majors": {"major_id": major.get("_id"),
									  "major_name": name}}}
			)
			print("Major added successfully.")
			break
		except Exception as e:
			print("An error occurred:")
			pprint(e)
			print("Please re-enter major information.")


def select_major(db):
	collection = db["majors"]
	found: bool = False
	name: str = ''
	while not found:
		name = input("Major's name--> ")
		name_count: int = collection.count_documents({"name": name})
		found = name_count == 1
		if not found:
			print("No major found by that name. Try again.")
	found_major = collection.find_one({"name": name})
	return found_major


def delete_major(db):
	collection = db["majors"]
	major = select_major(db)
	#ensure there are no student_majors with this major before deleting
	#...
	search = {
		"student_major":  {
			"$elemMatch": {
				"major_name": major.get("name")
			}
		}
	}
	declared_count = db.students.count_documents(search)
	if declared_count == 0:
		db.departments.update_one(
			{"abbreviation": major.get("department_abbreviation")},
			{"$pull": {"majors": {"major_name": major.get("name")}}}
		)
		deleted = collection.delete_one({"_id": major["_id"]})
		print(f"We just deleted: {deleted.deleted_count} majors")
	else:
		print(f"There are {declared_count} students declared to that major.\n"
			  f"Undeclare them first, then come back here to delete the major.")


def list_major(db):
	majors = db["majors"].find({}).sort("name", pymongo.ASCENDING)
	for major in majors:
		pprint(major)