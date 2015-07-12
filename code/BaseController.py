import tornado.web
import json

from DAO import MongoDAO

PAGE_FILE_NAME_SUFFIX = ".html"
class MethodDispatcher(tornado.web.RequestHandler):  
    def initialize(self):
        self.dao = MongoDAO()
    
    def _dispatch(self, method):
        print self.request.body
        data_dict = json.loads(self.request.body.decode("utf-8")) 
        self.write(getattr(self, method)(data_dict))
        self.flush()

    def _renderPage(self):
        page_file_name = self.request.path[1:] + PAGE_FILE_NAME_SUFFIX
        self.render(page_file_name)
   
    def get(self, method):
        try :
            self._renderPage()
        except Exception, e:
            raise tornado.web.HTTPError(404)
   
    def post(self, method):  
        self._dispatch(method)
        
class Utility:
    @staticmethod
    def convertIdListToItemList(dao, item_dict, id_list_key, item_list_key, collection_name):
        item_list = []
        for id in item_dict[id_list_key]:
            input_dto = {"filter" : {"_id" : id}}
            item_list.append(dao.excute("findOne", collection_name, input_dto)["item"])
        del item_dict[id_list_key]
        item_dict[item_list_key] = item_list

    @staticmethod
    def convertIdToItem(dao, item_dict, id_key, item_key, collection_name):
        input_dto = {"filter" : {"_id" : item_dict[id_key]}}
        item_dict[item_key] = dao.excute("findOne", collection_name, input_dto)["item"]
        del item_dict[id_key]
        
class ForendBaseController(MethodDispatcher):
    COLLECTION_NAME = ""
#    def prepare(self):
#        if not self.get_secure_cookie("customer_id"):
#            self.redirect("/forend/index")
        
    def getOptionalList(self, data_dict):
        pass
    
    def getBookingList(self, data_dict):
        pass
        
    def getBooking(self, data_dict):
        pass
        
    def makeBooking(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        item = data_dict
        item["customer_id"] = customer_id
        input_dto = {"documents" : [item]}
        return self.dao.excute("insert", self.COLLECTION_NAME, input_dto)
        
    def updateBooking(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        filter = {"customer_id" : customer_id,
                    "_id" : data_dict["_id"]}
        update_set = data_dict["update_set"]
        input_dto = {"filter" : filter, 
                           "update" : {"$set" : update_set}}
        return self.dao.excute("update", self.COLLECTION_NAME, input_dto)
        
    def cancelBooking(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        filter = {"customer_id" : customer_id,
                    "_id" : data_dict["_id"]}
        input_dto = {"filter" : filter}
        return self.dao.excute("delete", self.COLLECTION_NAME, input_dto)
        
class BackendBaseController(MethodDispatcher):
    COLLECTION_NAME = ""
#    def prepare(self):
#        if not self.get_secure_cookie("administrator_id"):
#            self.redirect("/backend/login")
    
    def addItem(self, data_dict):
        item_list = [data_dict]
        input_dto = {"documents" : item_list}
        return self.dao.excute("insert", self.COLLECTION_NAME, input_dto)

    def getAllItems(self, data_dict):
        input_dto = {"filter" : None}
        return self.dao.excute("find", self.COLLECTION_NAME, input_dto)

    def getOneItem(self, data_dict):
        input_dto = {"filter" : {"_id" : data_dict["_id"]}}
        return self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)

    def updateItem(self, data_dict):
        update_set = data_dict["update_set"]
        input_dto = {"filter" : {"_id" : data_dict["_id"]},
                           "update" : {"$set" : update_set}}
        return self.dao.excute("update", self.COLLECTION_NAME, input_dto)

    def deleteItem(self, data_dict):
        input_dto = {"filter" : {"_id" : data_dict["_id"]}}
        return self.dao.excute("delete", self.COLLECTION_NAME, input_dto)