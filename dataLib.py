# import mongodbConnect
from mongodbConnect import collection, client
from logs import logProcesses
# from ..job_scrapper import jobScrapper

def saveJobs(scrappedJobs):
    document_list = []
    # print(scrappedJobs)
    for key, value in scrappedJobs.items():
        checkCollection = collection.estimated_document_count() #Check if collection is empty
        if checkCollection > 0:
            count = collection.estimated_document_count({"name" : key, "link" : value}) # Check if data isnt already in DB
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
    lessThanOne = {"numberTimesPosted": {"$eq": 0}}
    postedOnceOrTwice = {"$or": [{"numberTimesPosted": {"$eq": 1}}, {"numberTimesPosted": {"$eq": 2}}]}
    if collection.estimated_document_count(lessThanOne) > 0:
        results = collection.find_one(lessThanOne)
        return results
    elif collection.estimated_document_count(postedOnceOrTwice) > 0:
        results = collection.find_one(postedOnceOrTwice)
        return results



def countData():
    filter_query = {"numberTimesPosted": {"$lte": 2}}
    results = collection.estimated_document_count(filter_query)
    # print(results)
    return results


def updatePostedJob(job):
    filter_query = {"name": job['name'], "link": job['link']}
    update_operation = { "$inc": {"numberTimesPosted": 1} }
    result = collection.update_one(filter_query, update_operation)
    return result.acknowledged


    


def deleteAllData():
    filter_query = {"numberTimesPosted": {"$lte": 2}}
    results = collection.delete_many(filter_query)
    # logProcesses(results.acknowledged) Log Later
    return results.acknowledged


def deleteOneData(jobID):
    filter_query = {"_id": jobID}
    results = collection.delete_one(filter_query)
    # logProcesses(results.acknowledged) Log later
    return results.acknowledged
# print(saveJobs())