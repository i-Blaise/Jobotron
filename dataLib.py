from mongodbConnect import MongoDBManager
from config_manager import get_config
from logs import logProcesses

def get_db_resources():
    return MongoDBManager.get_collection(), MongoDBManager.get_client()

def max_post_count():
    return get_config()["max_post_count"]

def saveJobs(scrappedJobs):
    collection, _ = get_db_resources()
    if collection is None:
        print("MongoDB collection not available. Skipping saveJobs.")
        return "Database Unavailable"

    document_list = []
    for key, value in scrappedJobs.items():
        filter = {"numberTimesPosted": {"$lte": max_post_count()}}
        checkCollection = collection.count_documents(filter) #Check if collection is empty
        if checkCollection > 0:
            count = collection.count_documents({"name" : key, "link" : value}) # Check if data isnt already in DB
            if count == 0:
                job_dict = dict(name = key, link = value, numberTimesPosted = 0)
                document_list.append(job_dict)
        else:
            job_dict = dict(name = key, link = value, numberTimesPosted = 0)
            document_list.append(job_dict)

    if not document_list:
        return 'No New Job'
    else:
        result = collection.insert_many(document_list)
        return result.acknowledged

def retrieveData():
    collection, _ = get_db_resources()
    if collection is None:
        return None
        
    neverPosted = {"numberTimesPosted": {"$eq": 0}}
    postedButRepostable = {"numberTimesPosted": {"$gt": 0, "$lte": max_post_count()}}

    if collection.count_documents(neverPosted) > 0:
        results = collection.find_one(neverPosted)
        return results
    elif collection.count_documents(postedButRepostable) > 0:
        results = collection.find_one(postedButRepostable)
        return results
    return None

def countData():
    collection, _ = get_db_resources()
    if collection is None:
        return 0
    filter_query = {"numberTimesPosted": {"$lte": max_post_count()}}
    # Use count_documents instead of estimated_document_count if the filter is important and collection is small
    # Or keep estimated if performance matters, but it doesn't take a filter in the same way
    return collection.count_documents(filter_query)

def updatePostedJob(job):
    collection, _ = get_db_resources()
    if collection is None:
        return False
    filter_query = {"name": job['name'], "link": job['link']}
    update_operation = { "$inc": {"numberTimesPosted": 1} }
    result = collection.update_one(filter_query, update_operation)
    return result.acknowledged

def deleteAllData():
    collection, _ = get_db_resources()
    if collection is None:
        return False
    filter_query = {"numberTimesPosted": {"$lte": max_post_count()}}
    results = collection.delete_many(filter_query)
    return results.acknowledged

def deleteOneData(jobID):
    collection, _ = get_db_resources()
    if collection is None:
        return False
    filter_query = {"_id": jobID}
    results = collection.delete_one(filter_query)
    return results.acknowledged