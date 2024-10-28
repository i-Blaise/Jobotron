from job_scrapper import jobScrapper, scrapJobDetails
from dataLib import retrieveData, countData, deleteAllData
from gemini_ai import AI_Summary
from createxpost import postJob



def startPoint():
    count = countData()
    if count >= 4:
        job = retrieveData()
        jobLink = job['link']
        jobDetails = scrapJobDetails(jobLink)
        twitterPost = AI_Summary(jobDetails["jobDetail"], jobDetails["link"])
        print(postJob(twitterPost))




print(startPoint())
    
# jobDetails = scrapJobDetails()
# print(jobDetails["link"])
# print(AI_Summary(jobDetails["jobDetail"], jobDetails["link"]))
# print(countData())
# print(deleteAllData())









# print(jobScrapper())

# print(retrieveData())