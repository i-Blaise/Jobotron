from job_scrapper import jobScrapper, scrapJobDetails
from dataLib import retrieveData, countData, deleteAllData



def startPoint():
    count = countData()
    if count >= 4:
        job = retrieveData()
        link = job['name']
        return link

    
print(scrapJobDetails())
# print(countData())
# print(deleteAllData())









# print(jobScrapper())

# print(retrieveData())