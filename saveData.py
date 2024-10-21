# import mongodbConnect
from mongodbConnect import collection
# from ..job_scrapper import jobScrapper

def saveJobs(scrappedJobs):
    document_list = []
    # print(scrappedJobs)
    for key, value in scrappedJobs.items():
        job_dict = dict(name = key, link = value, numberTimesPosted = 0)
        document_list.append(job_dict)
        
    result = collection.insert_many(document_list)
    print(result.acknowledged)
        



# print(saveJobs())