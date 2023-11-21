import pymongo
from pprint import pprint

def add_department(db):
    """
    Add a new department, making sure that we don't put in any duplicates,
    based on the department name.
    :param db:  The connection to the current database.
    :return:    None
    """
    collection = db["departments"]

    while True:
        try:
            name = input("Department name (String length 50)--> ")
            abbreviation = input("Abbreviation (String length 6)--> ")
            chair_name = input("Chair Name (String length 80)--> ")
            building = input("Building (String length 10)--> ")
            office = int(input("Office (Integer)--> "))
            description = input("Description (String length 80)--> ")

            department = {
                "name": name,
                "abbreviation": abbreviation,
                "chair_name": chair_name,
                "building": building,
                "office": office,
                "description": description
            }
            collection.insert_one(department)
            print("Department added successfully.")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            print("Please re-enter department information.")



def select_department(db):
    collection = db["departments"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Department's name-->")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": name})
    return found_department


def delete_department(db):
    department = select_department(db)
    departments = db["departments"]
    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments")


def list_department(db):
    departments = db["departments"].find({}).sort("name", pymongo.ASCENDING)
    for department in departments:
        pprint(department)