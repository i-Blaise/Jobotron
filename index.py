from job_scrapper import jobScrapper, scrapJobDetails
from dataLib import retrieveData, countData, deleteAllData
from gemini_ai import AI_Summary



def startPoint():
    count = countData()
    if count >= 4:
        job = retrieveData()
        link = job['name']
        return link



    
jobDetails = scrapJobDetails()
# print(jobDetails["link"])
print(AI_Summary(jobDetails["jobDetail"], jobDetails["link"]))
# print(countData())
# print(deleteAllData())









# print(jobScrapper())

# print(retrieveData())