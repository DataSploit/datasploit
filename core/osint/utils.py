from pymongo import MongoClient
from django.conf import settings

def save_record(domain, tid, key, data):
	client = MongoClient(settings.MONGO_HOSTNAME, 27017)
	db = client.database1
        d = {"targetname": domain, "taskId": tid, "record": {"type": key, "data": data}}
        result = db.domaindata.insert(d, check_keys=False)
        return result
