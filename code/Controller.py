from BaseController import *     
import os
import time

class ForendDefaultController(MethodDispatcher):
    def loginPost(self, data_dict):
        input_dto = {"filter" : data_dict}
        output_dto = self.dao.excute("isExist", "customer", input_dto)
        if output_dto["is_exist"]:
            self.set_cookie("customer_name", output_dto["username"])
            self.set_secure_cookie("customer_id", output_dto["_id"])
        return output_dto
        
    def registerPost(self, data_dict):
        input_dto = {"documents" : [data_dict]}
        return self.dao.excute("insert", "customer", input_dto)
        
    def logoutPost(self, data_dict):
        self.clear_cookie("customer_name")
        self.clear_cookie("customer_id")
        #self.redirect("/forend/index")
        output_dto = {"execute_result" : True}
        return output_dto
        
class ForendMyCenterController(MethodDispatcher):
#    def prepare(self):
#        if not self.get_secure_cookie("customer_id"):
#            self.redirect("/forend/index")
        
    def getMyInformation(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        input_dto = {"filter" : {"_id" : customer_id}}
        return self.dao.excute("findOne", "customer", input_dto)
        
    def updateMyInformation(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        update_set = data_dict["update_set"]
        input_dto = {"filter"  : {"_id" : customer_id}, 
                           "update" : {"$set" : update_set}}
        return self.dao.excute("update", "customer", input_dto)
        
class ForendRoomBookingController(ForendBaseController):
    COLLECTION_NAME = "roomBooking"
    def makeBooking(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        item = data_dict
        item["customer_id"] = customer_id
        input_dto = {"documents" : [item]}
        
        update_set = {"room_state" : "used"}
        temp_input_dto = {"filter" : {"_id" : data_dict["room_id"]},
                           "update" : {"$set" : update_set}}
        self.dao.excute("update", "room", temp_input_dto)
        
        return self.dao.excute("insert", self.COLLECTION_NAME, input_dto)
    
    def getOptionalList(self, data_dict):
        input_dto = {"filter" : {"room_state" : "available"}}
        return self.dao.excute("find", "room", input_dto)
        
    def getBookingList(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        filter = {"customer_id" : customer_id}
        input_dto = {"filter" : filter}
        output_dto =  self.dao.excute("find", self.COLLECTION_NAME, input_dto)
        for item in output_dto["item_list"]:
            Utility.convertIdToItem(self.dao, item, "room_id", "room_item", "room");
            Utility.convertIdToItem(self.dao, item["room_item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
        
    def getBooking(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        filter = {"customer_id" : customer_id, "_id" : data_dict["_id"]}
        input_dto = {"filter" : filter}
        output_dto = self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)
        Utility.convertIdToItem(self.dao, output_dto["item"], "room_id", "room_item", "room");
        Utility.convertIdToItem(self.dao, output_dto["item"]["room_item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
        
    def getCategoryOptionalList(self, data_dict):
        input_dto = {"filter" : {"room_state" : "available", "room_category_id" : data_dict["room_category_id"] }}
        return self.dao.excute("find", "room", input_dto)
        
class ForendMealBookingController(ForendBaseController):
    COLLECTION_NAME = "mealBooking"
    def getOptionalList(self, data_dict):
        input_dto = {"filter" : None}
        return self.dao.excute("find", "dishCategory", input_dto)

    def getBookingList(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        filter = {"customer_id" : customer_id}
        input_dto = {"filter" : filter}
        output_dto =  self.dao.excute("find", self.COLLECTION_NAME, input_dto)
        for item in output_dto["item_list"]:
            Utility.convertIdListToItemList(self.dao, item, "dish_category_id_list", "dish_category_item_list", "dishCategory");
        return output_dto
        
    def getBooking(self, data_dict):
        customer_id = self.get_secure_cookie("customer_id")
        filter = {"customer_id" : customer_id, "_id" : data_dict["_id"]}
        input_dto = {"filter" : filter}
        output_dto = self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)
        Utility.convertIdListToItemList(self.dao, output_dto["item"], "dish_category_id_list", "dish_category_item_list", "dishCategory");
        return output_dto
        
###################################################
        
class BackendDefaultController(MethodDispatcher):   
    def loginPost(self, data_dict):
        output_dto = {}
        if data_dict["username"] == "admin" and data_dict["password"] == "admin":
            self.set_cookie("administrator_name", "admin")
            self.set_secure_cookie("administrator_id", "10086")
            output_dto = {"excute_result" : True, "is_exist" : True}
        else:
            output_dto = {"excute_result" : True, "is_exist" : False}
        return output_dto
        
    def logoutPost(self, data_dict):
        self.clear_cookie("administrator_name")
        self.clear_cookie("administrator_id")
        #self.redirect("/backend/logout")
        output_dto = {"execute_result" : True}
        return output_dto
    
class BackendCustomerController(BackendBaseController):
    COLLECTION_NAME = "customer"
    
class BackendRoomController(BackendBaseController):
    COLLECTION_NAME = "room"
    def getAllItems(self, data_dict):
        input_dto = {"filter" : None}
        output_dto =  self.dao.excute("find", self.COLLECTION_NAME, input_dto)
        for item in output_dto["item_list"]:
            Utility.convertIdToItem(self.dao, item, "room_category_id", "room_category_item", "roomCategory");
        return output_dto
        
    def getOneItem(self, data_dict):
        filter = {"_id" : data_dict["_id"]}
        input_dto = {"filter" : filter}
        output_dto = self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)
        Utility.convertIdToItem(self.dao, output_dto["item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
    
class BackendCleanTaskController(BackendBaseController):
    COLLECTION_NAME = "cleanTask"
    def getAllItems(self, data_dict):
        input_dto = {"filter" : None}
        output_dto =  self.dao.excute("find", self.COLLECTION_NAME, input_dto)
        for item in output_dto["item_list"]:
            Utility.convertIdToItem(self.dao, item, "employee_id", "employee_item", "employee");
            Utility.convertIdToItem(self.dao, item, "room_id", "room_item", "room");
            Utility.convertIdToItem(self.dao, item["room_item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
        
    def getOneItem(self, data_dict):
        filter = {"_id" : data_dict["_id"]}
        input_dto = {"filter" : filter}
        output_dto = self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)
        Utility.convertIdToItem(self.dao, output_dto["item"], "employee_id", "employee_item", "employee");
        Utility.convertIdToItem(self.dao, output_dto["item"], "room_id", "room_item", "room");
        Utility.convertIdToItem(self.dao, output_dto["item"]["room_item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
    
class BackendEmployeeController(BackendBaseController):
    COLLECTION_NAME = "employee"
    
class BackendRoomBookingController(BackendBaseController):
    COLLECTION_NAME = "roomBooking"
    def getAllItems(self, data_dict):
        input_dto = {"filter" : None}
        output_dto =  self.dao.excute("find", self.COLLECTION_NAME, input_dto)
        for item in output_dto["item_list"]:
            Utility.convertIdToItem(self.dao, item, "room_id", "room_item", "room");
            Utility.convertIdToItem(self.dao, item, "customer_id", "customer_item", "customer");
            Utility.convertIdToItem(self.dao, item["room_item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
        
    def getOneItem(self, data_dict):
        filter = {"_id" : data_dict["_id"]}
        input_dto = {"filter" : filter}
        output_dto = self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)
        Utility.convertIdToItem(self.dao, output_dto["item"], "room_id", "room_item", "room");
        Utility.convertIdToItem(self.dao, output_dto["item"], "customer_id", "customer_item", "customer");
        Utility.convertIdToItem(self.dao, output_dto["item"]["room_item"], "room_category_id", "room_category_item", "roomCategory");
        return output_dto
    
class BackendMealBookingController(BackendBaseController):
    COLLECTION_NAME = "mealBooking"
    def getAllItems(self, data_dict):
        input_dto = {"filter" : None}
        output_dto =  self.dao.excute("find", self.COLLECTION_NAME, input_dto)
        for item in output_dto["item_list"]:
            Utility.convertIdToItem(self.dao, item, "customer_id", "customer_item", "customer");
            Utility.convertIdListToItemList(self.dao, item, "dish_category_id_list", "dish_category_item_list", "dishCategory");
        return output_dto

    def getOneItem(self, data_dict):
        input_dto = {"filter" : {"_id" : data_dict["_id"]}}
        output_dto = self.dao.excute("findOne", self.COLLECTION_NAME, input_dto)
        Utility.convertIdToItem(self.dao, output_dto["item"], "customer_id", "customer_item", "customer");
        Utility.convertIdListToItemList(self.dao, output_dto["item"], "dish_category_id_list", "dish_category_item_list", "dishCategory");
        return output_dto
    
class BackendDishCategoryController(BackendBaseController):
    COLLECTION_NAME = "dishCategory"
    
class BackendRoomCategoryController(BackendBaseController):
    COLLECTION_NAME = "roomCategory"
    
class FileUploadController(tornado.web.RequestHandler):
    UPLOAD_FILE_PATH = "/resources/upload/"
    def post(self):
        upload_path=os.path.join(os.path.dirname(__file__), self.UPLOAD_FILE_PATH[1:]) 
        file_metas=self.request.files["file"]  
        for meta in file_metas:
            filename = str(round(time.time(), 2)).replace(".", "_") + "." + meta['filename'].split(".")[1]
            filepath = os.path.join(upload_path,filename)
            with open(filepath, "wb") as up:  
                up.write(meta["body"])
            output_dto = {"excute_result" : True, "image_path" : self.UPLOAD_FILE_PATH + filename}
            self.write(output_dto)
