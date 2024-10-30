from job_scrapper import jobScrapper, scrapJobDetails
from dataLib import retrieveData, countData, deleteAllData, updatePostedJob
from gemini_ai import AI_Summary
from createxpost import postJob
import schedule
import time



def startPoint():
    count = countData() # Check DB to see if we have enough stored jobs to post for the day ===== 4 post per day ====
    if count >= 4:
        job = retrieveData() #If theres enough jobs, retrieve one
        jobLink = job['link']
        jobDetails = scrapJobDetails(jobLink) # Use link to scrap the details of the job
        twitterPost = AI_Summary(jobDetails["jobDetail"], jobDetails["link"]) #Run the details by Gemini AI to summerize it for a X
        if twitterPost:
            postResult = postJob(twitterPost)
            if postResult["status"]:
                updatePostedJob(job)
        # print(twitterPost)
        # print(postJob(twitterPost))




# startPoint()
    
# jobDetails = scrapJobDetails()
# print(jobDetails["link"])
# print(AI_Summary(jobDetails["jobDetail"], jobDetails["link"]))
# print(countData())
# print(deleteAllData())


# Schedule the job to run at four specific times each day
schedule.every().day.at("09:00").do(startPoint)
schedule.every().day.at("12:00").do(startPoint)
schedule.every().day.at("15:00").do(startPoint)
schedule.every().day.at("18:00").do(startPoint)
# schedule.every(5).seconds.do(countData)

while True:
    schedule.run_pending()
    time.sleep(1)


# print(jobScrapper())

# print(retrieveData())