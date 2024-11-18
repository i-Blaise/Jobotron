from job_scrapper import jobScrapper, scrapJobDetails
from dataLib import retrieveData, countData, deleteAllData, updatePostedJob, deleteOneData
from gemini_ai import AI_Summary, jobTips, adviceAndMotivation
from createxpost import postJob
import schedule
import time
from logs import logProcesses
from datetime import datetime



def startPoint():
    count = countData() # Check DB to see if we have enough stored jobs to post for the day ===== 4 post per day ====
    if count >= 4:
        job = retrieveData() #If theres enough jobs, retrieve one
        jobLink = job['link']
        jobDetails = scrapJobDetails(jobLink) # Use link to scrap the details of the job
        
        # return jobDetails
        expirationDate = jobDetails["closingDate"].strip()
        # return expirationDate
        expired = True if has_date_elapsed(expirationDate) else False

        if expired == True:
            deleteOneData(job["_id"])
            jobName = job["name"]
            print(f"{jobName} job has been deleted because it's expired")
            startPoint()
        
        twitterPost = AI_Summary(jobDetails["jobDetail"], jobDetails["link"]) #Run the details by Gemini AI to summerize it for a X
        # return print(twitterPost)
        # return twitterPost
        if twitterPost:
            postResult = postJob(twitterPost)
            if postResult["status"]:
                updatePostedJob(job)
                print("Job Tweeted")

    else:
        jobScrapper()
        result = {
            "status": False,
            "response": "DB results less than 4 documents || New Jobs Scrapped"
        }
        logProcesses(result['response'])
        print("DB results less than 4 documents || New Jobs Scrapped")
        startPoint()
        # print(twitterPost)
        # print(postJob(twitterPost))






# def begin():
#     count = countData()
#     while




def has_date_elapsed(date_str):
    check = False if date_str == 'False' else ''
    if check == False:
        return False
    # Parse the date string (DD/MM/YYYY) into a datetime object
    input_date = datetime.strptime(date_str, "%d/%m/%Y")
    
    # Get the current date without the time part
    current_date = datetime.now().date()
    
    # Compare input date with the current date
    if input_date.date() < current_date:
        return True  # Date has elapsed (i.e., it is in the past)
    else:
        return False  # Date has not elapsed (i.e., it is today or in the future)




def tweetJobTips():
    JobTipsTweet = jobTips()
    postJob(JobTipsTweet)
    currentDate = datetime.now()
    stringDate = currentDate.strftime('%m/%d/%Y  %X')
    print("Job Tip Tweeted at: "+ stringDate)


def tweetMotivations():
    motivationTweet = adviceAndMotivation()
    postJob(motivationTweet)
    currentDate = datetime.now()
    stringDate = currentDate.strftime('%m/%d/%Y  %X')
    print("Job Advice/Motivation Tweeted at: "+ stringDate)







# print(tweetJobTips())
print(tweetMotivations())

print(startPoint())
# print(scrapJobDetails())
# print(jobScrapper())
# print(retrieveData())

# startPoint()
    
# jobDetails = scrapJobDetails()
# print(jobDetails["link"])
# print(AI_Summary(jobDetails["jobDetail"], jobDetails["link"]))
# print(countData())
# print(deleteAllData())


# Schedule the job to run at four specific times each day
# schedule.every().day.at("09:00").do(startPoint)
# schedule.every().day.at("12:00").do(startPoint)
# schedule.every().day.at("15:00").do(startPoint)
# schedule.every().day.at("18:00").do(startPoint)


# schedule.every().day.at("07:30").do(tweetMotivations)
# schedule.every().day.at("13:00").do(tweetJobTips)
# schedule.every().day.at("17:00").do(tweetMotivations)
# schedule.every().day.at("20:30").do(tweetJobTips)

# schedule.every(30).seconds.do(startPoint)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


# print(jobScrapper())

# print(retrieveData())