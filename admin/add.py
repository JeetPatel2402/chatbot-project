import re
import os
import json
def add(fil,query,response):
    abs_path=os.path.abspath(os.getcwd())
    abs_pathd=os.path.join(abs_path,'data')
    abs_path=os.path.join(abs_pathd,fil)
    with open(abs_path ,'r') as feedjson:
        feeds=json.load(feedjson)
    entry={"message":query,"response":response}
    feeds.append(entry)
    
    with open(abs_path ,'w') as feedjson:
        json.dump(feeds,feedjson)
    if fil=='previous_chats.json':
        r='previous'
    elif fil=='guest.json':
        r='guest'
    else:
        r='student'
    for f in os.listdir(abs_pathd):
        if r in f and '.pickle' in f:
            path=os.path.join(abs_pathd,f)
            os.remove(path)
def update(fil,query,response):
    add(fil,query,response)