# import pymongo
# import sys
# import json

# def get_connection():
#     db_name=None
#     try:
#         connection_url=pymongo.MongoClient("mongodb://localhost:27017/")
#         db_name=connection_url["automation_config"]
#         print(db_name)
#     except Exception as exception:
#         print(exception)
#     return db_name

# def insert_single_document(collection_name, query, projection=None):
#     collection_data=None
#     try:
#         db_name=get_connection()
#         collection_name=db_name[collection_name]
#         print(collection_name)
#         collection_data=collection_name.insert_one(query, projection)    
#         print(collection_data)
#     except Exception as exception:
#         print(exception)
#     return collection_data

# def get_single_document(collection_name, query, projection=None):
#     collection_data=None
#     try:
#         db_name=get_connection()
#         collection_name=db_name[collection_name]
#         print(collection_name)
#         collection_data=collection_name.find_one(query, projection)    
#         print(collection_data)
#     except Exception as exception:
#         print(exception)
#     return collection_data

# def update_single_document(collection_name, query, projection=None):
#     collection_data=None
#     try:
#         db_name=get_connection()
#         collection_name=db_name[collection_name]
#         print(collection_name)
#         collection_data=collection_name.update_one(query, projection)    
#         print(collection_data)
#     except Exception as exception:
#         print(exception)
#     return collection_data

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python script.py <json>")
#         sys.exit(1)
#     json_file_path = sys.argv[1]
#     try:
#         with open(json_file_path) as file:
#             json_content = file.read()
#             json_data = json.loads(json_content)
#             insert_single_document("config", json_data)
#     except json.JSONDecodeError:
#         print("Invalid JSON format")
#         sys.exit(1)
#     # Chequeando get
#     # get_single_document("config",{"name":"abc"},{"_id":0})
#     # Chequeando update
#     # update_single_document("config", {"username": "Pedro"}, {"$set": {"name":"user_config"}})
#     # get_single_document("config", {"name":"user_config"}, {"_id":0})