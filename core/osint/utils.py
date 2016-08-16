from pymongo import MongoClient
import config

def save_record(domain, tid, key, data):
	client = MongoClient(config.mongo_uri)
	db = client.database1
        d = {"targetname": domain, "taskId": tid, "record": {"type": key, "data": data}}
        result = db.domaindata.insert(d, check_keys=False)
        return result
