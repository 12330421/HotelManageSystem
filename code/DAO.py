from pymongo import MongoClient
from bson.objectid import ObjectId

DATABASE_SERVER_IP = "127.0.0.1"
DATABASE_SERVER_PORT = 27017
DATABASE_NAME = "HotelManageSystem"
 
class MongoDAO():
    def __init__(self):
        self.connection = MongoClient(DATABASE_SERVER_IP, DATABASE_SERVER_PORT)

    def convertStringIdToObjectId(self, dto):
        if "filter" in dto.keys() and dto["filter"] and  "_id" in dto["filter"].keys():
            dto["filter"]["_id"] = ObjectId(dto["filter"]["_id"])

            
    def convertObjectIdToStringId(self, dto):
        if "item" in dto.keys():
            dto["item"]["_id"] = str(dto["item"]["_id"])
        elif "item_list" in dto.keys():
            for i in xrange(len(dto["item_list"])):
                dto["item_list"][i]["_id"] = str(dto["item_list"][i]["_id"])
        
    def excute(self, operation_name, collection_name, input_dto):
        output_dto = {}
        try:
            self.convertStringIdToObjectId(input_dto)
    #       print "DAO input_dto: ", input_dto
            collection = self.connection[DATABASE_NAME][collection_name]
            getattr(self, operation_name)(collection, input_dto, output_dto)
            self.convertObjectIdToStringId(output_dto)
    #        print "DAO output_dto: ", output_dto
            output_dto["excute_result"] = True
        except Exception, e:
            print e
            output_dto["excute_result"] = False
        finally:
            return output_dto

    def insert(self, collection, input_dto, output_dto):
        collection.insert_many(input_dto["documents"])

    def find(self, collection, input_dto, output_dto):
        item_list = collection.find(input_dto["filter"])
        temp_list = []
        for item in item_list:
            temp_list.append(item)
        output_dto["item_list"] = temp_list
        
    def findOne(self, collection, input_dto, output_dto):
        item = collection.find_one(input_dto["filter"])
        if item:
            output_dto["item"] = item
        else:
            output_dto["item"] = {}
            
    def findOneWithColumnFilter(self, collection, input_dto, output_dto):
        temp_item = collection.find_one(input_dto["filter"])
        item = {}
        for key in input_dto["column_filter"]:
            item[key] = temp_item[key]
        output_dto["item"] = item
    
    def findWithColumnFilter(self, collection, input_dto, output_dto):
        temp_item_list = collection.find(input_dto["filter"])
        item_list = []
        for temp_item in temp_item_list:
            temp_dict = {}
            for key in input_dto["column_filter"]:
                temp_dict[key] = temp_item[key]
            item_list.append(temp_dict)
        output_dto["item_list"] = item_list
        
    def delete(self, collection, input_dto, output_dto):
        collection.find_one_and_delete(input_dto["filter"])
        
    def update(self, collection, input_dto, output_dto):
        collection.find_one_and_update(input_dto["filter"], input_dto["update"])

    def count(self, collection, input_dto, output_dto):
        number_of_document = collection.count(input_dto["filter"])
        output_dto["number_of_item"] = number_of_document
        
    def isExist(self, collection, input_dto, output_dto):
        item = collection.find_one(input_dto["filter"])
        if item:
            output_dto["is_exist"] = True
            output_dto["username"] = item["username"]
            output_dto["_id"] = str(item["_id"])
        else:
            output_dto["is_exist"] = False
    
    def __del__ (self):
        self.connection.close()
        
