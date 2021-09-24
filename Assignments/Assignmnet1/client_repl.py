import grpc

import dbreplicator_pb2
import dbreplicator_pb2_grpc

import os
import time
import subprocess

channel = grpc.insecure_channel('localhost:50051')

stub = dbreplicator_pb2_grpc.dbReplicatorStub(channel)


import re
def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.read()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line

if __name__ == '__main__':
    # create slot
    cmd1 = 'pg_recvlogical -d college --slot test_slot --create-slot -P wal2json'
    os.system(cmd1)
    # start the slot for repliaction
    cmd= 'pg_recvlogical -d college --slot test_slot --start -o pretty-print=1 -f output.txt'    
    subprocess.Popen([cmd], shell=True)    
    print("slot started for replication")

    # read output.txt file
    time.sleep(2)
    logfile = open("output.txt","r")
    loglines = follow(logfile)

    # iterate over the generator
    for line in loglines:
        data = line
        msg = dbreplicator_pb2.dbRequest()
        msg.query=data
        response = stub.replicate(msg)
        print(response.responsemsg)
    
