# import mongodbConnect
from mongodbConnect import collection, client
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
    filter_query = {"numberTimesPosted": {"$lte": 2}}
    update_query = {"numberTimesPosted": 1}
    results = collection.find_one(filter_query)
    return results



def countData():
    filter_query = {"numberTimesPosted": {"$lte": 2}}
    results = collection.estimated_document_count(filter_query)
    return results


def deleteAllData():
    filter_query = {"numberTimesPosted": {"$lte": 2}}
    results = collection.delete_many(filter_query)
    return results.acknowledged
# print(saveJobs())