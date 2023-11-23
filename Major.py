import pymongo
from pprint import pprint

def create_major_schema(db):
	major_validator={
		 'validator': {
			'$jsonSchema': {
				'bsonType': "object",
				'description': 'A specific area of study in which a student chooses to specialize',
				'required': ['name'],
				'additionalProperties': False,
				'properties': {
					'_id': {},
					'name': {
						'bsonType': 'string',
						'description': 'given name of the major'
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
	while True:
		try:
			name = input("Major name--> ")

			major = {
				"name": name
			}
			collection.insert_one(major)
			print("Major added successfully.")
			break
		except Exception as e:
			print("An error occurred:", str(e))
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
	major = select_major(db)
	majors = db["majors"]
	deleted = majors.delete_one({"_id": major["_id"]})
	print(f"We just deleted: {deleted.deleted_count} majors")


def list_major(db):
	majors = db["majors"].find({}).sort("name", pymongo.ASCENDING)
	for major in majors:
		pprint(major)