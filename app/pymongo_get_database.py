from pymongo import MongoClient

def get_database(username, password):
    hostname='192.168.1.76'
    port=27017
    CONNECTION_STRING="mongodb://"+username+":"+password+"@"+hostname+"/datos"
    client = MongoClient(CONNECTION_STRING)
    return client["datos"]

if __name__ == "__main__":
    db = get_database()
    