import grpc
from concurrent import futures
import time
import json
import pymongo

import dbreplicator_pb2
import dbreplicator_pb2_grpc

def connecttoMongo():
    myclient = pymongo.MongoClient("mongodb+srv://sayali:sayali@cluster0.wpv6a.mongodb.net/college?retryWrites=true&w=majority")
    mydb = myclient["college"]
    return mydb

class dbReplicatorServicer(dbreplicator_pb2_grpc.dbReplicatorServicer):
    def replicate(self, request, context):
        response = dbreplicator_pb2.dbResponse()
        data = json.loads(request.query)
        #connect to mongo
        mydb = connecttoMongo()
        # print(data["change"])
        for param in data["change"]:
            if(param["kind"] == "insert"):
                # print("insert")
                tablename = param["table"]
                insertquery ={}
                for colname, colvalue in zip(param["columnnames"], param["columnvalues"]):
                    insertquery.update({colname: colvalue})
                tablename = param["table"]
                mycol = mydb[tablename]
                mycol.insert_one(insertquery)
            elif(param["kind"] == "update"):
                # print('update')
                tablename = param["table"]
                updatequery ={}
                for colname, colvalue in zip(param["columnnames"], param["columnvalues"]):
                    updatequery.update({colname: colvalue})
                del updatequery["id"] 
                myquery = {param["oldkeys"]["keynames"][0] : param["oldkeys"]["keyvalues"][0]}
                mycol = mydb[tablename]
                mycol.update_one(myquery, {"$set": updatequery})


                
            elif(param["kind"] == "delete"):
                #delete operation here
                # print("insidde delete")
                tablename = param["table"]
                mycol = mydb[tablename]
                myquery = {param["oldkeys"]["keynames"][0] : param["oldkeys"]["keyvalues"][0]}
                mycol.delete_one(myquery)

        response.responsemsg = 'recieved : query'
     
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

dbreplicator_pb2_grpc.add_dbReplicatorServicer_to_server(dbReplicatorServicer(), server)

print('Starting server Listening on port 50051')
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
