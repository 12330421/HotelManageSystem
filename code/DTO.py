for mongodb:
    input_dto = { "collection_name" : not None  ,
                        "operation_name" : "insert", 
                        "filter" :  dict,  #ex: {'_id': 665}
                        "update" : dict, #not None for update_many operation, ex: {'$inc': {'count': 1}, '$set': {'done': True}}
                        "documents" : list of dict, #not None for insert_many operation
                      }
                      
    output_dto = {"excute_result" :   True or False ,
                         "item_list" : list of dict #not None for find operation
                         "item" : dict #not None for find_one operations
                         "number_of_item": int  #not None for count operation
                         "is_exist" : boolean #not None for isExist operation
                         "name" : string #for cookie
                         "id" : int  #for secret cookie
                        }